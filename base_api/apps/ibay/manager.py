# -*- coding: utf-8 -*-
import asyncio
import datetime
import functools
import json

import socketio
from sqlalchemy.ext.asyncio import AsyncSession
from base_api.apps.ibay.database import IbayDatabase
from .enums import OrderStatus
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
        # CREATING TRANSACTION
        print(product, "PRODUCT")
        print(product.wallet_id)
        print("BEFORE CREATING")
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
        order_status = OrderStatus.NEW if status else OrderStatus.FAILED
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

    async def change_status(self, message: dict, status: OrderStatus, session: AsyncSession):
        order_id = message.get("order_id")
        order = await self.database.get_order_by_id(order_id, session)
        print(order.txn_hash, "TNX HASH IN CHANGE STATUS")
        updated_order = await self.database.update_order_for_delivery(tnx_hash=order.txn_hash, order_status=status, db=session)
        updated_message = {
            "order_id": order_id,
            "status": status
        }
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
        if status.FAILED:
            print("SHOULD RETURN BACK MONEY to BUYER")
