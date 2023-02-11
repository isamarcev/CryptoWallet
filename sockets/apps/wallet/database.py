# -*- coding: utf-8 -*-
import json

from aioredis import Redis


class WalletDatabase:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def connect_user(self, user_id, sid):
        users = await self.redis.get("users_online")
        print(user_id, sid, "USERID SID")
        try:
            users = json.loads(users)
        except:
            pass

        if users:
            users[user_id] = sid
            users = json.dumps(users)
            await self.redis.set("users_online", users)
        else:
            users = {user_id: sid}
            users = json.dumps(users)
            await self.redis.set("users_online", users)


    async def get_users(self):
        users = await self.redis.get("users_online")
        if users:
            users = json.loads(users)
            return users
        else:
            return []

    async def disconnect_user(self, user_id: str):
        users = await self.redis.get("users_online")
        users = json.loads(users)
        users.pop(user_id)
        users = json.dumps(users)
        await self.redis.set("users_online", users)
