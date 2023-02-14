from ibay.apps.dataabase import OrderDatabase
from ibay.apps.manager import OrderManager
from ibay.apps.order_handlers import OrderHandler


async def get_order_database() -> OrderDatabase:

    return OrderDatabase()


async def get_order_manager() -> OrderManager:
    database = await get_order_database()
    return OrderManager(database)


async def get_order_handler() -> OrderHandler:
    manager = await get_order_manager()
    return OrderHandler(manager)