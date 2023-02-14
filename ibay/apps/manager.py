import asyncio
import time

import aiohttp

from ibay.apps.dataabase import OrderDatabase
from ibay.ibay_producer import IbayProducer


class OrderManager:

    def __init__(self, database: OrderDatabase, producer: IbayProducer):
        self.database = database
        self.producer = producer


    async def start_delivery_process(self, message, session):
        instance = await self.database.create_order(message, session)
        order_id = message.get("order_id")
        requests = await self.send_requests()
        if requests:
            await self.database.update_to_delivery(order_id, session)
            answer_message = {"order_id": order_id}
            await self.producer.publish_message(
                "change_to_delivery",
                answer_message
            )



    async def request(self):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.google.com/") as resp:
                return resp.status

    async def send_requests(self):
        start_timestamp = time.time()
        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.create_task(session.get("https://www.google.com/")) for i in range(10000)]
            results = await asyncio.gather(*tasks, return_exceptions=True)
        response = {r.status for r in results}
        task_time = round(time.time() - start_timestamp, 2)
        print(task_time)
        if 200 in set(response) and len(response) == 1:
            return True
        return False



