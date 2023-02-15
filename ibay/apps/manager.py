import asyncio
import time

import aiohttp
from sqlalchemy.ext.asyncio import AsyncSession

from ibay.apps.dataabase import OrderDatabase
from ibay.apps.enums import OrderStatus
from ibay.ibay_producer import IbayProducer


class OrderManager:

    def __init__(self, database: OrderDatabase, producer: IbayProducer):
        self.database = database
        self.producer = producer

    async def start_delivery_process(self, message, session):
        print(message, type(message))
        instance = await self.database.create_order(message, session)
        order_id = message.get("order_id")
        requests = await self.send_requests()
        answer_message = {"order_id": order_id}
        if requests:
            await self.database.update_to_delivery(order_id, session)
            await self.producer.publish_message(
                "change_to_delivery",
                answer_message
            )
        else:
            await self.database.update_to_failed(order_id, session)
            await self.producer.publish_message(
                "change_to_failed",
                answer_message
            )

    @staticmethod
    async def send_requests():
        start_timestamp = time.time()
        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.create_task(session.get("https://www.google.com/")) for i in range(10)]
            results = await asyncio.gather(*tasks, return_exceptions=True)
        print([r for r in results])
        response = {r.status for r in results}
        print(response)
        task_time = round(time.time() - start_timestamp, 2)
        print(task_time)
        if 200 in set(response) and len(response) == 1:
            return True
        return False

    async def get_last_order(self, db: AsyncSession):
        order = await self.database.get_first_order(db)
        return order

    async def feedback(self, order_id, status: OrderStatus, db: AsyncSession):
        updated_order = await self.database.update_to_status(order_id, status, db)
        answer_message = {"order_id": order_id, "status": status}
        await self.producer.publish_message(
            "feedback_from_delivery",
            answer_message
        )



