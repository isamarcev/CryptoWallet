import socketio

# create a Socket.IO server
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins="*")


@sio.event
async def connect(sid, environ, auth):
    print('connect ', sid)
    print('auth', auth)
    print('dima connected')
    sio.save_session(sid, {'sid': sid})
    print('session = ', sio.get_session(sid))
    await sio.emit('new_message', sid, to=sid)


@sio.event
async def disconnect(sid):
    print('disconnect')


@sio.event
def connect_to_chat(sid):
    print('connect ', sid)


@sio.event
def disconnect_from_chat(sid):
    print('disconnect ', sid)


@sio.event
async def new_message(sid):
    print('new message')
    await sio.emit('new_message')
