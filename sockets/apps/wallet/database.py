# -*- coding: utf-8 -*-
import json

from aioredis import Redis


class WalletDatabase:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def connect_user(self, user_id, sid):
        users = await self.redis.get("users_online")
        try:
            users = json.loads(users)
        except:
            pass
        if users:
            if users.get(user_id):
                users[user_id].append(sid)
            else:
                users[user_id] = [sid]
            users = json.dumps(users)
            await self.redis.set("users_online", users)
        else:
            users = {user_id: [sid]}
            users = json.dumps(users)
            await self.redis.set("users_online", users)


    async def get_users(self):
        users = await self.redis.get("users_online")
        if users:
            users = json.loads(users)
            return users
        else:
            return []

    async def disconnect_user(self, user_id: str, sid: str):
        users = await self.redis.get("users_online")
        users = json.loads(users)
        current_user_session = users.get(user_id)
        if current_user_session:
            current_user_session.remove(sid)
        if not current_user_session:
            users.pop(user_id)
        users = json.dumps(users)
        await self.redis.set("users_online", users)
