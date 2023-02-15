import datetime
from typing import Type

from ibay.apps.enums import OrderStatus
from ibay.apps.models import Order, order_table
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, update, select


class OrderDatabase:

    def __init__(self, order_model: Type[Order]):
        self.order_model = order_model

    async def create_order(self, order: dict, db: AsyncSession):
        order_instance = self.order_model(order_number=order.get("order_id"))
        db.add(order_instance)
        await db.commit()
        return order_instance

    async def update_to_delivery(self, order_id: str, db: AsyncSession):
        query = await db.execute(
            update(self.order_model).where(order_table.c.order_number == order_id)
            .values({"status": OrderStatus.DELIVERY})
        )
        print(query)
        await db.commit()


    async def update_to_failed(self, order_id: str, db: AsyncSession):
        query = await db.execute(
            update(self.order_model).where(order_table.c.order_number == order_id)
            .values({"status": OrderStatus.FAILED})
        )
        print(query)
        await db.commit()

    async def update_to_status(self, order_id: str, status: OrderStatus, db: AsyncSession):
        query = await db.execute(
            update(self.order_model).where(order_table.c.order_number == order_id)
            .values({"status": status})
        )
        print(query)
        await db.commit()



    async def get_first_order(self, db: AsyncSession):
        query = await db.execute(
            select(order_table).where(
                order_table.c.status == "DELIVERY"
            ).order_by(order_table.c.datetime)
        )
        result = query.scalars().first()
        return result if result else None
