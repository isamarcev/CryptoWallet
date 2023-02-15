from ibay.apps.dataabase import OrderDatabase
from ibay.apps.manager import OrderManager
from ibay.apps.models import Order
from ibay.ibay_producer import IbayProducer


async def get_order_database() -> OrderDatabase:
    return OrderDatabase(Order)

async def get_producer() -> IbayProducer:
    return IbayProducer()


async def get_order_manager() -> OrderManager:
    database = await get_order_database()
    producer = await get_producer()
    return OrderManager(database, producer)

