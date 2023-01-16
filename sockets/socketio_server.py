import socketio

# create a Socket.IO server
sio = socketio.AsyncServer()


@sio.event
def connect_to_chat(sid, environ, auth):
    print('connect ', sid)


@sio.event
def disconnect_from_chat(sid):
    print('disconnect ', sid)


@sio.event
async def new_message(sid, data):
    pass
