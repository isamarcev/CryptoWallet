import asyncio
import logging
from threading import Thread

from aio_pika import connect, ExchangeType, connect_robust
from aio_pika.abc import AbstractIncomingMessage
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# from base_api.apps.ethereum.tasks import check_transactions_by_block
# from base_api.config.db import SessionLocal, get_session
from ibay.config.settings import settings
# from base_api.apps.ethereum.dependencies import get_ethereum_manager


logger = logging.getLogger(__name__)


async def check_transaction_by_block(message: AbstractIncomingMessage):

    # db = session.connection()
    # ethereum_manager = await get_ethereum_manager()
    print(message.body)
    async with message.process():
        logger.info(f"Got new block: {message.body}")

        # await ethereum_manager.check_transaction_in_block(message.body.decode("utf-8"), db)
        # check_transactions_by_block.apply_async(args=[message.body.decode()])
        # check_transactions_by_block.apply_async(args=[f"{message.body.decode()}"])
        # await new_message(message.body)

async def main() -> None:
    # Perform connection
    connection = await connect_robust(settings.rabbit_url)

    async with connection:
        # Creating a channel
        print("CONNECTING")
        channel = await connection.channel()
        # await channel.set_qos(prefetch_count=1)

        new_block_exchange = await channel.declare_exchange(
            "new_order",
            ExchangeType.FANOUT,
        )

        # Declaring queue
        new_block_queue = await channel.declare_queue(exclusive=True)

        # Binding the queue to the exchange
        await new_block_queue.bind(new_block_exchange)

        # Start listening the queue
        await new_block_queue.consume(check_transaction_by_block)

        print(" [*] Waiting for logs. To exit press CTRL+C")
        await asyncio.Future()


base_api_consumer_thread = Thread(target=asyncio.run, args=(main(),))