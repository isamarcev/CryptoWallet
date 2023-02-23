# -*- coding: utf-8 -*-
import asyncio
from typing import Awaitable, Callable
import aio_pika
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from sqladmin import Admin

from base_api.base_api_consumer import base_api_consumer_thread
from base_api.config.db import init_db, engine
from base_api.config.settings import settings
from base_api.config.utils.sqlalchemy_admin import UserAdmin, PermissionAdmin, ProductAdmin, OrderAdmin, WalletAdmin, \
    TransactionAdmin, MessageAdmin, authentication_backend
from services.rabbit.lifetime import init_rabbit, shutdown_rabbit
from services.redis.dependencies import get_redis


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
        await init_db()
        redis = await get_redis()
        await redis.delete("users_online")
        await FastAPILimiter.init(redis)
        await init_rabbit(app)
        try:
            connection = await aio_pika.connect_robust(settings.rabbit_url)
            await connection.close()
        except Exception:
            await asyncio.sleep(10)
        base_api_consumer_thread.start()
        admin = Admin(app, engine, authentication_backend=authentication_backend)
        admin.add_view(UserAdmin)
        admin.add_view(PermissionAdmin)
        admin.add_view(ProductAdmin)
        admin.add_view(OrderAdmin)
        admin.add_view(WalletAdmin)
        admin.add_view(TransactionAdmin)
        admin.add_view(MessageAdmin)
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
        await shutdown_rabbit(app)

    return _shutdown
