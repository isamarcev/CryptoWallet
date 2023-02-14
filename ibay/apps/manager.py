import asyncio
import time

import aiohttp


class OrderManager:

    def __init__(self, database):
        self.database = database

    async def request(self):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.google.com/") as resp:
                return resp.status

    async def send_requests(self):
        start_timestamp = time.time()

        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.create_task(session.get("https://www.google.com/")) for i in range(10)]
            results = await asyncio.gather(*tasks, return_exceptions=True)
        response = {r.status for r in results}
        task_time = round(time.time() - start_timestamp, 2)
        print(task_time)
        # results = await asyncio.gather(*requests, return_exceptions=True)
        print(set(response))
        print("SUCCESS")



