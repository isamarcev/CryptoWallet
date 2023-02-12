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
            print(users, "USER DEVICES IN WALLET DB0")
            print(users.get(user_id), "GET LIST USER ID")
            if users.get(user_id):
                print(users[user_id], "USERS[USERID] 1")
                users[user_id].append(sid)
                print(users[user_id], "USERS[USERID] 2")

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
        # current_user_session.clear()
        users = json.dumps(users)
        await self.redis.set("users_online", users)
