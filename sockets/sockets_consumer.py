import asyncio
import logging
from threading import Thread

import aio_pika
from aio_pika import ExchangeType, connect
from aio_pika.abc import AbstractIncomingMessage

from sockets.config.settings import settings


async def on_message(message: AbstractIncomingMessage) -> None:
    async with message.process():
        print(message.body)


async def main() -> None:
    # Perform connection
    connection = await connect(settings.rabbit_url)

    async with connection:
        # Creating a channel
        channel = await connection.channel()
        # await channel.set_qos(prefetch_count=1)



        new_message_exchange = await channel.declare_exchange(
            "new_message", ExchangeType.FANOUT,
        )

        # Declaring queue
        new_message_queue = await channel.declare_queue(exclusive=True)

        # Binding the queue to the exchange
        await new_message_queue.bind(new_message_exchange)

        # Start listening the queue
        await new_message_queue.consume(on_message)






        print(" [*] Waiting for logs. To exit press CTRL+C")
        await asyncio.Future()


socket_consumer_thread = Thread(target=asyncio.run, args=(main(),))
