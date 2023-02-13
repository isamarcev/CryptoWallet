# -*- coding: utf-8 -*-
from sqlalchemy.ext.asyncio import AsyncSession
from base_api.apps.ibay.database import IbayDatabase
from .exeptions import WalletIsUndefined
from .schemas import CreateProduct
from ..ethereum.database import EthereumDatabase
from ..users.models import User
from ...config.storage import Storage


class IbayManager:

    def __init__(self, database: IbayDatabase, storage: Storage, eth_database: EthereumDatabase):
        self.database = database
        self.storage = storage
        self.eth_database = eth_database

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
