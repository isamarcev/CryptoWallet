import json

from aioredis import Redis


class ChatUsers:

    def __init__(self, redis: Redis):
        self.redis = redis

    async def connect_user(self, session):
        auth = session.get('auth')
        sid = session.get('sid')
        users = await self.redis.get('chat_users')
        print(type(users))
        try:
            users = json.loads(users)
        except:
            pass
        print('2')
        if users:
            users.append(session)
            users = json.dumps(users)
            await self.redis.set('chat_users', users)
        else:
            users = [session]
            users = json.dumps(users)
            await self.redis.set('chat_users', users)

    async def get_users(self):
        users = await self.redis.get('chat_users')
        if users:
            users = json.loads(users)
            return users
        else:
            return []

    async def get_chat_history(self):
        history = await self.redis.get('message_list')
        if not history:
            history = []
        history = json.loads(history)
        print(type(history))
        return history

    async def disconnect_user(self, session):
        users = await self.redis.get('chat_users')
        users = json.loads(users)
        users.remove(session)
        users = json.dumps(users)
        await self.redis.set('chat_users', users)

