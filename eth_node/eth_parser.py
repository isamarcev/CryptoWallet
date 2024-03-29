# -*- coding: utf-8 -*-
import asyncio
import datetime
import json
from pathlib import Path

from aio_pika import DeliveryMode, ExchangeType, Message, connect_robust
from pydantic import BaseSettings
from websockets import connect
from yarl import URL


BASE_DIR = Path(__file__).parent


class Settings(BaseSettings):

    # Variables for RabbitMQ
    rabbit_host: str = "localhost"
    rabbit_port: int = 5672
    rabbit_user: str = "guest"
    rabbit_pass: str = "guest"
    rabbit_vhost: str = "/"

    # Ethereum settings
    infura_api_url: str
    infura_api_key: str


    @property
    def rabbit_url(self) -> URL:
        """
        Assemble RabbitMQ URL from settings.

        :return: rabbit URL.

        """
        return URL.build(
            scheme="amqp",
            host=self.rabbit_host,
            port=self.rabbit_port,
            user=self.rabbit_user,
            password=self.rabbit_pass,
            path=self.rabbit_vhost,
        )

    class Config:
        """
        Configure the application.
        """

        env_file = BASE_DIR / ".env.prod"
        env_file_encoding = "utf-8"


settings = Settings()


async def start_parse():
    await asyncio.sleep(1)
    async with connect(settings.infura_api_url) as websocket:
        await websocket.send(
            '{"jsonrpc": "2.0", "id": 1, "method": "eth_subscribe", "params": ["newHeads"]}',
        )
        subscription_response = await websocket.recv()
        print(f"Parser start successfully {subscription_response}")

        while True:
            try:
                message = await asyncio.wait_for(websocket.recv(), timeout=2)
                response = json.loads(message)
                block_number = response["params"]["result"]["number"]
                print(
                    f'{datetime.datetime.now().strftime("%H:%M:%S")} '
                    f"-- Got new block form Ethereum Network -- {block_number}",
                )

                # publish new message with aio-pika
                connection = await connect_robust(settings.rabbit_url)

                async with connection:
                    channel = await connection.channel()

                    new_blocks_exchange = await channel.declare_exchange(
                        "new_block",
                        ExchangeType.FANOUT,
                    )

                    message = Message(
                        f"{block_number}".encode(),
                        delivery_mode=DeliveryMode.PERSISTENT,
                    )

                    # Sending the message
                    await new_blocks_exchange.publish(message, routing_key="info")

            except Exception:
                pass


if __name__ == "__main__":
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # loop.run_until_complete(start_parse())
    asyncio.run(start_parse())
