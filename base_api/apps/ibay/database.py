import datetime
from typing import Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from base_api.apps.ethereum.models import Wallet
from base_api.apps.ibay.enums import OrderStatus
from base_api.apps.ibay.models import Product, product as product_table
from base_api.apps.ibay.models import Order, order as order_table
from base_api.apps.ibay.schemas import CreateProduct
from base_api.apps.users.models import User


class IbayDatabase:

    def __init__(self, product: Type[Product], order: Type[Order]):
        self.order_model = order
        self.product_model = product

    async def create_order(self, order_data, db) -> Order:
        order_instance = self.order_model(**order_data)
        db.add(order_instance)
        await db.commit()
        await db.refresh(order_instance)
        order = await db.execute(
            select(self.order_model).where(order_table.c.product_id == order_instance.product_id).options(selectinload(self.order_model.product))
        )
        result = order.scalars().first()
        return result

    async def update_order_for_delivery(self, tnx_hash: str, order_status: OrderStatus, db: AsyncSession):
        query = (
            order_table.update().where(order_table.c.txn_hash == tnx_hash).values({"status": order_status})
        )
        await db.execute(query)
        await db.commit()
        if order_status == OrderStatus.DELIVERY:
            request = await db.execute(
                select(self.order_model).where(order_table.c.txn_hash == tnx_hash)
            )
            order = request.first()._asdict().get("Order")
            return order

    async def get_user_orders(self, user: User, db: AsyncSession):
        order = await db.execute(
            select(self.order_model).where(order_table.c.user_id == user.id).options(selectinload(self.order_model.product))
            .order_by(order_table.c.datetime.desc())
        )
        result = order.scalars().all()
        return result

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

    async def get_product_by_id(self, product_id: str, db: AsyncSession):
        request = await db.execute(
            product_table.select().where(product_table.c.id == product_id)
        )
        result = request.first()
        # product = self.product_model(**result._asdict())
        return result
