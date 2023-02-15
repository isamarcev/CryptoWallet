import asyncio
from random import choice
from threading import Thread

from ibay.apps.dataabase import OrderDatabase
from ibay.apps.dependencies import get_order_manager
from ibay.apps.enums import OrderStatus
from ibay.apps.manager import OrderManager
from ibay.apps.models import Order
from ibay.config.database import get_session
from ibay.config.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from ibay.ibay_producer import IbayProducer

DATABASE_URL = str(settings.postgres_url)
engine = create_async_engine(DATABASE_URL, future=True)
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class OrderHandler:

    def __init__(self, manager: OrderManager):
        self.order_manager = manager
        # self.produ

    async def delivery(self):
        session = async_session()
        # while True:
        #     orders = await self.order_manager.get_last_order(session)
        #     print(orders)
        #     if orders:
        #         choices = choice([True, False])
        #         status = OrderStatus.COMPLETE if choices else OrderStatus.RETURN
        #         await self.order_manager.feedback(orders.id, status, session)
        #     await asyncio.sleep(5)
        await asyncio.sleep(10)
        print("DELIVERY")


order_handler = OrderHandler(OrderManager(OrderDatabase(Order), IbayProducer()))

order_thread = Thread(target=asyncio.run, args=(order_handler.delivery(),))

