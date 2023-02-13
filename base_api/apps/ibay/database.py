import datetime
from typing import Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from base_api.apps.ethereum.models import Wallet
from base_api.apps.ibay.models import Product, product as product_table
from base_api.apps.ibay.schemas import CreateProduct
from base_api.apps.users.models import User


class IbayDatabase:
    def __init__(self, product: Type[Product]):
        self.product_model = product

    async def create_product(self, product: CreateProduct, db: AsyncSession):
        product_instance = self.product_model(**product.dict(), date_created=datetime.datetime.now())
        db.add(product_instance)
        await db.commit()
        return product_instance

    async def get_products(self, user: User, db: AsyncSession):
        result = await db.execute(
            select(self.product_model).order_by(product_table.c.date_created.desc()).options(selectinload(self.product_model.wallet))
        )
        results = result.scalars().all()
        return results
