# -*- coding: utf-8 -*-
import asyncio
import datetime
import functools
import json

import socketio
from sqlalchemy.ext.asyncio import AsyncSession
from base_api.apps.ibay.database import IbayDatabase
from .enums import OrderStatus
from .models import Order
from ..ethereum.web3_client import EthereumClient
from ...base_api_producer import BaseApiProducer
from .exeptions import WalletIsUndefined, ProductDoesNotExistsOrAlreadySold
from .schemas import CreateProduct, Orders, CreateOrder
from ..ethereum.database import EthereumDatabase
from base_api.apps.ethereum.exeptions import WalletCreatingError, InvalidWalletImport, WalletAlreadyExists, \
    WalletIsNotDefine, WalletAddressError
from ..users.models import User
from aioredis import Redis
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
        print(txn_hash, "TXH HASH AFTER SEND")
        # txn_hash = "0x95a30e1c955c53c6a6a95e872886e297a812fd04043cf1672e5ab775831d29e8"
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
                            status=new_order.status,
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
        except:
            pass

        redis_orders = await self.redis.get("orders_transaction")
        if redis_orders:
            orders_transaction = json.loads(redis_orders)
            orders_transaction.append(txn_hash)
            orders_transaction = json.dumps(orders_transaction)
        else:
            orders_transaction = json.dumps([txn_hash])
        await self.redis.set("orders_transaction", orders_transaction)

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
        # tnx_hash = "0x95a30e1c955c53c6a6a95e872886e297a812fd04043cf1672e5ab775831d29e8"
        order = await self.database.update_order_for_delivery(tnx_hash, order_status, db)
        if order and status:
            message = {
                "order_id": str(order.id),
            }
            print(message)
            await self.producer.publish_message(
                "new_order",
                message=message,
            )

    async def change_status(self, message: dict, status: str, session: AsyncSession):
        order_id = message.get("order_id")
        order = await self.database.get_order_by_id(order_id, session)
        print(order.txn_hash, "TNX HASH IN CHANGE STATUS")
        updated_order = await self.database.update_order_for_delivery(tnx_hash=order.txn_hash, order_status=status, db=session)
        await self.update_front_end_status(order_id, order, status)

        # updated_message = {
        #     "order_id": order_id,
        #     "status": status
        # }
        # try:
        #     users_online = await self.redis.get("users_online")
        #     users = json.loads(users_online)
        #     online_devices = users.get(str(order.user))
        #     if online_devices:
        #         for device in online_devices:
        #             await self.socket_manager.emit("update_order_status",
        #                                            data=updated_message,
        #                                            room=device)
        # except:
        #     pass
        if status == OrderStatus.FAILED:
            print("SHOULD RETURN BACK MONEY to BUYER")

    async def finish_order(self, message: dict, db: AsyncSession):
        order_id = message.get("order_id")
        status = message.get("status")

        order = await self.database.get_order_by_id(order_id, db)
        print(order.txn_hash, "TNX HASH IN CHANGE STATUS")
        updated_order = await self.database.update_order_for_delivery(tnx_hash=order.txn_hash,
                                                                      order_status=status,
                                                                      db=db)
        if status == "COMPLETE":
            await self.update_front_end_status(order_id, order, status)

        if status == "RETURN":
            await self.return_money_to_buyer(order, db)

        print(message)
        pass


    async def update_front_end_status(self, order_id, order, status, returning_txn = None):
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
        except:
            pass

    async def return_money_to_buyer(self, order: Order, db: AsyncSession):
        type(order)
        wallet_buyer = await self.eth_database.get_wallet_by_public_key(order.buyer_wallet, db)
        print(wallet_buyer)
        product_owner_wallet = order.product.address
        print(product_owner_wallet)
        owner_wallet = await self.eth_database.get_wallet_by_id(str(product_owner_wallet), db)
        print(owner_wallet)
        loop = asyncio.get_running_loop()
        txn_hash = await loop.run_in_executor(None, functools.partial(self.client.sync_send_transaction,
                                                                      from_address=owner_wallet.public_key,
                                                                      to_address=wallet_buyer.public_key,
                                                                      amount=order.product.price,
                                                                      private_key=owner_wallet.privet_key))
        print(txn_hash)

        await self.database.update_order_for_returning(str(order.id), txn_hash, "RETURN", db)
        await self.update_front_end_status(str(order.id), order, "RETURN", txn_hash)
        # returning_txn = await self.redis.get("returning_txn")
        # await self.database.update_order_for_delivery()
        # if returning_txn:
        #     list_txn = json.loads(returning_txn)
        #     list_txn.append(txn_hash.hex())
        # else:
        #     list_txn = [txn_hash.hex()]
        # await self.redis.set("returning_txn", list_txn)


