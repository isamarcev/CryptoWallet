import socketio

sio = socketio.AsyncServer()


@sio.event
def connect(sid, environ, auth):
    print('connect ', sid)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


@sio.event
async def my_event(sid, data):
    pass
