from aioredis import Redis


class ChatUsers:

    def __int__(self, redis: Redis):
        self.redis = redis

    async def connect_user(self, session):
        auth = session.get('auth')
        sid = session.get('sid')
        try:
            users = await self.redis.get('chat_users')
            users.appand(session)
            await self.redis.set('chat_users', users)
        except:
            users = [session]
            await self.redis.set('chat_users', users)

    async def get_users(self):
        try:
            users = await self.redis.get('chat_users')
            return users
        except:
            return []



