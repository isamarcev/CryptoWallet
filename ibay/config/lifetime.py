# -*- coding: utf-8 -*-
import asyncio
from typing import Awaitable, Callable

import aio_pika
from aio_pika import connect_robust
from fastapi import FastAPI

from ibay.ibay_consumer import base_api_consumer_thread
# from base_api.config.db import init_db
from ibay.config.settings import settings
from services.rabbit.lifetime import init_rabbit, shutdown_rabbit


def register_startup_event(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application startup.

    This function uses fastAPI app to store data
    in the state, such as db_engine.

    :param app: the fastAPI application.
    :return: function that actually performs actions.

    """

    @app.on_event("startup")
    async def _startup() -> None:  # noqa: WPS430
        # await init_db()
        # await init_redis(app)
        await init_rabbit(app)
        try:
            connection = await aio_pika.connect_robust(settings.rabbit_url)
            await connection.close()
        except Exception:
            await asyncio.sleep(10)
        base_api_consumer_thread.start()
    return _startup


def register_shutdown_event(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application's shutdown.

    :param app: fastAPI application.
    :return: function that actually performs actions.

    """

    @app.on_event("shutdown")
    async def _shutdown() -> None:  # noqa: WPS430
        pass
        # await shutdown_redis(app)
        await shutdown_rabbit(app)

    return _shutdown
