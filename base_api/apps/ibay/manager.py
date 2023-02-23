# -*- coding: utf-8 -*-
import asyncio
import datetime
import functools
import json

import socketio
from sqlalchemy.ext.asyncio import AsyncSession
from base_api.apps.ibay.database import IbayDatabase
from ..ethereum.web3_client import EthereumClient
from ...base_api_producer import BaseApiProducer
from .exeptions import WalletIsUndefined, ProductDoesNotExistsOrAlreadySold, TheSameWalletError
from .schemas import CreateProduct, Orders, CreateOrder
from ..ethereum.database import EthereumDatabase
from base_api.apps.ethereum.exeptions import WalletIsNotDefine
from ..users.models import User
from aioredis import Redis

from ...config.settings import settings
from ...config.storage import Storage


class IbayManager:

    def __init__(self,
                 database: IbayDatabase,
                 storage: Storage,
                 eth_database: EthereumDatabase,
                 producer: BaseApiProducer,
                 client: EthereumClient,
                 redis: Redis,
                 socket_manager: socketio.AsyncAioPikaManager):
        self.database = database
        self.storage = storage
        self.producer = producer
        self.eth_database = eth_database
        self.client = client
        self.redis = redis
        self.socket_manager = socket_manager

    async def create_order(self, user: User, db: AsyncSession, order: CreateOrder):
        user_wallet = await self.eth_database.get_wallet_by_public_key(order.from_wallet, db)
        if not user_wallet or user_wallet.user != user.id:
            raise WalletIsNotDefine()
        product = await self.database.get_product_by_id(str(order.product_id), db)
        if user_wallet.id == product.wallet_id:
            raise TheSameWalletError()
        if not product or product.is_sold:
            raise ProductDoesNotExistsOrAlreadySold()
        product_wallet = await self.eth_database.get_wallet_by_id(str(product.wallet_id), db)
        loop = asyncio.get_running_loop()
        txn_hash = await loop.run_in_executor(None,
                                              functools.partial(
                                                  self.client.sync_send_transaction,
                                                  from_address=order.from_wallet,
                                                  to_address=str(product_wallet.public_key),
                                                  amount=product.price,
                                                  private_key=user_wallet.privet_key))
        order_data = {
            "txn_hash": txn_hash,
            "datetime": datetime.datetime.now(),
            "buyer_wallet": user_wallet.public_key,
            "product_id": order.product_id,
            'user': user.id
        }
        new_order = await self.database.create_order(order_data, db)
        order_data = Orders(id=new_order.id,
                            txn_hash=new_order.txn_hash,
                            datetime=new_order.datetime,
                            status="NEW",
                            product=new_order.product).json()
        order_data = json.loads(order_data)
        try:
            users_online = await self.redis.get("users_online")
            users = json.loads(users_online)
            online_devices = users.get(str(user.id))
            if online_devices:
                for device in online_devices:
                    await self.socket_manager.emit("new_order_show",
                                                   data=order_data,
                                                   room=device)
        except Exception:
            pass
        await self.put_order_to_redis("orders_transaction", txn_hash)

    async def put_order_to_redis(self, queue, transaction_hash):
        """Put order to redis with recursion if Exeprtion raise"""
        try:
            redis_orders = await self.redis.get(queue)
            if redis_orders:
                orders_transaction = json.loads(redis_orders)
                orders_transaction.append(transaction_hash)
                orders_transaction = json.dumps(orders_transaction)
            else:
                orders_transaction = json.dumps([transaction_hash])
            await self.redis.set("orders_transaction", orders_transaction)
        except Exception as e:
            print("ERROR IN REDIS ", e)
            await asyncio.sleep(2)
            await self.put_order_to_redis(queue, transaction_hash)

    async def create_product(self, product: CreateProduct, user: User, db: AsyncSession):
        wallet = await self.eth_database.get_wallet_by_public_key(product.address, db)
        if wallet:
            if not wallet.user == user.id:
                raise WalletIsUndefined()
            product.image = await self.storage.upload_image(product.image, 'products', [150, 200])
            product.address = wallet.id
            created_product = await self.database.create_product(product, db)
            created_product.address = wallet.public_key
            product = {
                "title": created_product.title,
                "address": created_product.address,
                "price": created_product.price,
                "image": created_product.image
            }
            await self.socket_manager.emit("show_new_product", data=product)
        else:
            raise WalletIsUndefined()

    async def get_products(self, user: User, db: AsyncSession):
        return await self.database.get_products(user, db)

    async def get_user_orders(self, user: User, db: AsyncSession):
        return await self.database.get_user_orders(user, db)

    async def send_order_to_delivery(self, tnx_hash: str, status: bool, db: AsyncSession):
        order_status = "NEW" if status else "FAILED"
        order = await self.database.update_order_for_delivery(tnx_hash, order_status, db)
        if order and status:
            message = {
                "order_id": str(order.id),
            }
            await self.producer.publish_message(
                "new_order",
                message=message,
            )

    async def change_status_with_redis(self, message: dict, status: str, session: AsyncSession, redis: Redis):
        order_id = message.get("order_id")
        order = await self.database.get_order_by_id(order_id, session)
        await self.database.update_order_for_delivery(tnx_hash=order.txn_hash, order_status=status, db=session)
        await self.update_front_end_status_with_redis(order_id, order, status, redis)

    async def update_front_end_status_with_redis(self, order_id, order, status, redis, returning_txn=None):
        updated_message = {
            "order_id": order_id,
            "status": status
        }
        if returning_txn:
            updated_message["returning_txn"] = returning_txn
        try:
            users_online = await redis.get("users_online")
            users = json.loads(users_online)
            online_devices = users.get(str(order.user))
            if online_devices:
                for device in online_devices:
                    await self.socket_manager.emit("update_order_status",
                                                   data=updated_message,
                                                   room=device)
        except Exception as e:
            print("ERROR in UPDATE FRONT END ", e)
            pass

    async def update_front_end_status(self, order_id, order, status, returning_txn=None):
        updated_message = {
            "order_id": order_id,
            "status": status
        }
        if returning_txn:
            updated_message["returning_txn"] = returning_txn
        try:
            users_online = await self.redis.get("users_online")
            users = json.loads(users_online)
            online_devices = users.get(str(order.user))
            if online_devices:
                for device in online_devices:
                    await self.socket_manager.emit("update_order_status",
                                                   data=updated_message,
                                                   room=device)
        except Exception as e:
            print("ERROR in UPDATE FRONT END ", e)
            pass

    async def finish_order_with_redis(self, order: dict, db: AsyncSession, redis: Redis):
        status = order.get("status")
        order_id = order.get("order_id")
        if status == "RETURN":
            print("FINISH OREDER WITH REDIS STATUS RETURN =", status)
            await self.return_money_to_buyer_with_redis(order, db, redis)
        elif status == "COMPLETE":
            print("FINISH OREDER WITH REDIS STATUS COMPLETE= ", status)
            order = await self.database.get_order_by_id(order_id, db)
            await self.database.update_order_for_delivery(tnx_hash=order.txn_hash,
                                                          order_status=status,
                                                          db=db)
            await self.update_front_end_status_with_redis(order_id, order, status, redis)

    async def return_money_to_buyer_with_redis(self, order_income: dict, db: AsyncSession, redis: Redis):
        order = await self.database.get_order_by_id(order_income.get("order_id"), db)
        wallet_buyer = await self.eth_database.get_wallet_by_public_key(order.buyer_wallet, db)
        product_owner_wallet = order.product.address
        owner_wallet = await self.eth_database.get_wallet_by_id(str(product_owner_wallet), db)
        commission = await self.get_commission_of_returning(order.txn_hash)
        amount_of_returning = order.product.price - (commission * 0.015)
        loop = asyncio.get_event_loop()
        txn_hash = await loop.run_in_executor(
            None, functools.partial(self.client.sync_send_transaction,
                                    from_address=owner_wallet.public_key,
                                    to_address=wallet_buyer.public_key,
                                    amount=amount_of_returning,
                                    private_key=owner_wallet.privet_key))

        fee_for_service_owner = await loop.run_in_executor(
            None, functools.partial(self.client.sync_send_transaction,
                                    from_address=wallet_buyer.public_key,
                                    to_address=settings.owner_public_key,
                                    amount=(commission * 1.5),
                                    private_key=wallet_buyer.privet_key))
        commission_tnx = await redis.get("commission_tnx")
        try:
            commission_list = json.loads(commission_tnx)
            commission_list.append(fee_for_service_owner)
        except Exception:
            commission_list = [fee_for_service_owner]
        await redis.set("commission_tnx", json.dumps(commission_list))

        await self.database.update_order_for_returning(
            str(order.id), txn_hash, order_income.get("status"), db)

        await self.update_front_end_status_with_redis(
            str(order.id), order, "RETURN", redis, txn_hash)

    async def get_commission_of_returning(self, tnx_hash: str):
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None, functools.partial(self.client.sync_get_transaction_receipt,
                                    txn_hash=tnx_hash,
                                    ))
        gas_price = result.get("effectiveGasPrice")
        gas_used = result.get("gasUsed")
        commission = gas_price * gas_used * (0.000000001 ** 2)
        return commission
