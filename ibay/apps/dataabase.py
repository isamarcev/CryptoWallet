import datetime
from typing import Type

from ibay.apps.enums import OrderStatus
from ibay.apps.models import Order, order_table
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, update


class OrderDatabase:

    def __init__(self, order_model: Type[Order]):
        self.order_model = order_model

    async def create_order(self, order: dict, db: AsyncSession):
        order["datetime"] = datetime.datetime.fromtimestamp(order["datetime"])
        order_instance = self.order_model(**order)
        db.add(order_instance)
        await db.commit()
        return order_instance

    async def update_to_delivery(self, order_id: str, db: AsyncSession):
        query = await db.execute(
            update(self.order_model).where(order_table.c.order_id == order_id)
            .values({"status": OrderStatus.DELIVERY})
        )
        print(query)
        await db.commit()
