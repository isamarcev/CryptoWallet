# -*- coding: utf-8 -*-
import socketio

# create a Socket.IO server
from sockets.apps.chat.dependencies import get_user_db
from sockets.apps.wallet.dependencies import get_users_online_db

# socket_manager = socketio.AsyncRedisManager("redis://localhost")
from sockets.config.settings import settings

socket_manager = socketio.AsyncAioPikaManager(settings.rabbit_url)

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins="*", client_manager=socket_manager)



@sio.event
async def connect(sid, environ, auth):
    print(sid)
    await sio.save_session(sid, {"auth": auth, "sid": sid})
    users_online_db = await get_users_online_db()
    session = await sio.get_session(sid)
    await users_online_db.connect_user(auth.get("user_id"), sid)
    if auth.get("url") == "/chat":
        sio.enter_room(sid, "chat")
        db = await get_user_db()
        await db.connect_user(session)
        users = await db.get_users()
        history = await db.get_chat_history()
        await sio.emit("get_history", history, to=sid)
        await sio.emit("get_online_users", users)



@sio.event
async def disconnect(sid):
    print("disconnect")
    session = await sio.get_session(sid)
    auth = session.get("auth")
    if auth.get("url") == "/chat":
        sio.leave_room(sid, "chat")
        db = await get_user_db()
        await db.disconnect_user(session)
        users = await db.get_users()
        await sio.emit("get_online_users", users)
    users_online_db = await get_users_online_db()
    await users_online_db.disconnect_user(auth.get("user_id"))







