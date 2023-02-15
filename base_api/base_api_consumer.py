import asyncio
import json
import logging
from threading import Thread

from aio_pika import connect, ExchangeType, connect_robust
from aio_pika.abc import AbstractIncomingMessage
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from base_api.apps.ethereum.tasks import check_transactions_by_block
from base_api.apps.ibay.dependencies import get_ibay_manager
from base_api.config.db import SessionLocal, get_session
from base_api.config.settings import settings
from base_api.apps.ethereum.dependencies import get_ethereum_manager
from ibay.apps.enums import OrderStatus

logger = logging.getLogger(__name__)


#create DB session
DATABASE_URL = str(settings.postgres_url)
engine = create_async_engine(DATABASE_URL, future=True)
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def check_transaction_by_block(message: AbstractIncomingMessage):
    async with message.process():
        logger.info(f"Got new block: {message.body}")
        check_transactions_by_block.apply_async(args=[message.body.decode()])


async def change_to_delivery_status(message: AbstractIncomingMessage):
    db = async_session()
    ibay_manager = await get_ibay_manager()
    async with message.process():
        logger.info(f"Got event to change status to DELIVERY")
        await ibay_manager.change_status(message.body.decode(), OrderStatus.DELIVERY, db)


async def change_to_failed_status(message: AbstractIncomingMessage):
    print("CHANGE TO FAILED MESSAGE")
    db = async_session()
    ibay_manager = await get_ibay_manager()
    async with message.process():
        logger.info(f"Got event to change status to DELIVERY")
        await ibay_manager.change_status(json.loads(message.body.decode()), OrderStatus.FAILED, db)


async def main() -> None:
    # Perform connection
    connection = await connect_robust(settings.rabbit_url)

    async with connection:
        # Creating a channel
        print("CONNECTING")
        channel = await connection.channel()
        # await channel.set_qos(prefetch_count=1)

        new_block_exchange = await channel.declare_exchange(
            "new_block",
            ExchangeType.FANOUT,
        )

        change_to_delivery = await channel.declare_exchange(
            "change_to_delivery",
            ExchangeType.FANOUT
        )

        change_to_failed = await channel.declare_exchange(
            "change_to_failed",
            ExchangeType.FANOUT
        )



        # Declaring queue
        new_block_queue = await channel.declare_queue(exclusive=True)
        change_to_delivery_queue = await channel.declare_queue(exclusive=True)
        change_to_failed_queue = await channel.declare_queue(exclusive=True)

        # Binding the queue to the exchange
        await new_block_queue.bind(new_block_exchange)
        await change_to_delivery_queue.bind(change_to_delivery)
        await change_to_failed_queue.bind(change_to_failed)

        # Start listening the queue
        await new_block_queue.consume(check_transaction_by_block)
        await change_to_delivery_queue.consume(change_to_delivery_status)
        await change_to_failed_queue.consume(change_to_failed_status)

        print(" [*] Waiting for logs. To exit press CTRL+C")
        await asyncio.Future()


base_api_consumer_thread = Thread(target=asyncio.run, args=(main(),))