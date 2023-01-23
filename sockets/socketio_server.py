import socketio

# create a Socket.IO server
from sockets.apps.chat.dependencies import get_user_db

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins="*")


@sio.event
async def connect(sid, environ, auth):
    await sio.save_session(sid, {"auth": auth, "sid": sid})
    if auth.get('url') == '/chat':
        print('chat!!!')
        sio.enter_room(sid, 'chat')
        db = await get_user_db()
        session = await sio.get_session(sid)
        print(session)
        await db.connect_user(session)
        users = await db.get_users()
        history = await db.get_chat_history()
        await sio.emit('get_history', history, to=sid)
        await sio.emit('get_online_users', users)
    # await sio.emit('new_message', sid, to=sid)
    # await sio.emit('new_message', sid)


@sio.event
async def disconnect(sid):
    print('disconnect')
    session = await sio.get_session(sid)
    auth = session.get('auth')
    if auth.get('url') == '/chat':
        sio.leave_room(sid, 'chat')
        db = await get_user_db()
        await db.disconnect_user(session)
        users = await db.get_users()
        await sio.emit('get_online_users', users)


@sio.event
def disconnect_from_chat(sid):
    print('disconnect ', sid)


@sio.event
async def new_message(sid):
    print('new message')
    await sio.emit('new_message')
