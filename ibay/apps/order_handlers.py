from ibay.apps.manager import OrderManager


class OrderHandler:

    def __init__(self, manager: OrderManager,):
        self.manager = manager


    async def getting_order(self, message):
        pass