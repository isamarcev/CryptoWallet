# -*- coding: utf-8 -*-
import json

from aioredis import Redis


class ChatUsers:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def connect_user(self, session):
        users = await self.redis.get("chat_users")
        try:
            users = json.loads(users)
        except:
            pass
        if users:
            users.append(session)
            users = list(users)
            users = json.dumps(users)
            await self.redis.set("chat_users", users)
        else:
            users = [session]
            users = json.dumps(users)
            await self.redis.set("chat_users", users)

    async def get_users(self):
        users = await self.redis.get("chat_users")
        if users:
            users = json.loads(users)
            return users
        else:
            return []

    async def get_chat_history(self):
        history = await self.redis.get("message_list")
        if not history:
            history = []
        history = json.loads(history)
        return history

    async def disconnect_user(self, session):
        users = await self.redis.get("chat_users")
        users = json.loads(users)
        users.remove(session)
        users = json.dumps(users)
        await self.redis.set("chat_users", users)
