import socketio

# create a Socket.IO server
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins="*")


@sio.event
def connect(sid, environ):
    print('connect ', sid)
    print('dima connected')


@sio.event
def connect_to_chat(sid):
    print('connect ', sid)


@sio.event
def disconnect_from_chat(sid):
    print('disconnect ', sid)


@sio.event
async def new_message(sid, data):
    pass
