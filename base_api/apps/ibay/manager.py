# -*- coding: utf-8 -*-
import asyncio
import datetime
import functools
import json
from sqlalchemy.ext.asyncio import AsyncSession
from base_api.apps.ibay.database import IbayDatabase
from base_api.apps.ibay.scheme import CreateOrder
from .enums import OrderStatus
from ..ethereum.web3_client import EthereumClient
from ...base_api_producer import BaseApiProducer
from .exeptions import WalletIsUndefined, ProductDoesNotExistsOrAlreadySold
from .schemas import CreateProduct
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
                 redis: Redis):
        self.database = database
        self.storage = storage
        self.producer = producer
        self.eth_database = eth_database
        self.client = client
        self.redis = redis

    async def create_order(self, user: User, db: AsyncSession, order: CreateOrder):
        user_wallet = await self.eth_database.get_wallet_by_public_key(order.from_wallet, db)
        if not user_wallet or (user_wallet.user) != (user.id):
            raise WalletIsNotDefine()
        product = await self.database.get_product_by_id(str(order.product_id), db)
        if not product or product.is_sold:
            raise ProductDoesNotExistsOrAlreadySold()
        # CREATING TRANSACTION
        # loop = asyncio.get_running_loop()
        # txn_hash = await loop.run_in_executor(None,
        #                                       functools.partial(
        #                                           self.client.sync_send_transaction,
        #                                           from_address=order.from_address,
        #                                           to_address=product.wallet_id,
        #                                           amount=product.price,
        #                                           private_key=user_wallet.privet_key))
        txn_hash = "0x95a30e1c955c53c6a6a95e872886e297a812fd04043cf1672e5ab775831d29e8"
        order_data = {
            "txn_hash": txn_hash,
            "datetime": datetime.datetime.now(),
            "buyer_wallet": user_wallet.public_key,
            "product_id": order.product_id,
        }
        new_order = await self.database.create_order(order_data, db)

        redis_orders = await self.redis.get("orders_transaction")
        if redis_orders:
            orders_transaction = json.loads(redis_orders)
            orders_transaction.append(txn_hash)
        else:
            orders_transaction = json.dumps([txn_hash])
        await self.redis.set("orders_transaction", orders_transaction)



        return {"Good": "FOOD"}

    async def create_product(self, product: CreateProduct, user: User, db: AsyncSession):
        wallet = await self.eth_database.get_wallet_by_public_key(product.address, db)
        if wallet:
            if not wallet.user == user.id:
                raise WalletIsUndefined()
            product.image = await self.storage.upload_image(product.image, 'products', [150, 200])
            product.address = wallet.id
            created_product = await self.database.create_product(product, db)
            created_product.address = wallet.public_key
            return created_product
        else:
            raise WalletIsUndefined()

    async def get_products(self, user: User, db: AsyncSession):
        return await self.database.get_products(user, db)


    async def send_order_to_delivery(self, tnx_hash: str, status: bool, db: AsyncSession):
        print(tnx_hash, type(tnx_hash), "TNX HASH IN IBAY DELIVERY MANAGER") #TEST
        order_status = OrderStatus.DELIVERY if status else OrderStatus.FAILED
        tnx_hash = "0x95a30e1c955c53c6a6a95e872886e297a812fd04043cf1672e5ab775831d29e8"
        order = await self.database.update_order_for_delivery(tnx_hash, order_status, db)
        if order:
            message = {
                "order_id": str(order.id),
                "datetime": order.datetime.timestamp(),
                "TEST": "TEST"
            }
            print(message)
            await self.producer.publish_message(
                "new_order",
                message=message,
            )
