import json

import socketio

# sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins="*")
from sockets.socketio_server import sio


# async def new_message(message):
#     message = json.loads(message)
#     await sio.emit('new_message', message, room='chat')
