
from typing import Awaitable, Callable
from fastapi import FastAPI

from sockets.config.db import init_db
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
        await init_db()

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


    return _shutdown