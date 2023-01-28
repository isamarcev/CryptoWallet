# -*- coding: utf-8 -*-
import socketio
from fastapi import FastAPI

from sockets.config.lifetime import register_shutdown_event, register_startup_event
from sockets.socketio_server import sio


def get_application() -> FastAPI:
    app_ = FastAPI()
    socket_app = socketio.ASGIApp(socketio_server=sio, socketio_path="socket.io")
    app_.mount("/ws", socket_app)
    register_startup_event(app_)
    register_shutdown_event(app_)

    return app_


app = get_application()
