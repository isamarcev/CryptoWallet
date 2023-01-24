import json
from datetime import datetime

from aioredis import Redis
from sqlalchemy import asc
from sqlalchemy.ext.asyncio import AsyncSession

from base_api.apps.chat.models import Message
from base_api.apps.chat.schemas import MessageCreate, MessageDetail, MessageDetail1
from base_api.apps.users.models import User
from base_api.apps.users.models import user as user_table
from base_api.apps.chat.models import message as message_table


class ChatDatabase:
    """
        :param message_model: message_model

    """
    def __init__(self, message_model: Message, redis: Redis):
        self.message_model = message_model
        self.redis = redis

    async def create_message(self, message: MessageCreate, db: AsyncSession, user: User):
        message_instance = Message(**message.dict(), user=user.id, datetime=datetime.now())
        db.add(message_instance)
        await db.commit()
        result = await db.execute(
            message_table.select().order_by(message_table.c.datetime.desc()).limit(10)
        )

        new = []
        for message in result:
            message = message._asdict()
            message['id'] = str(message['id'])
            message['user_id'] = str(message['user_id'])
            message['datetime'] = str(message['datetime'])
            new.append(message)
        new = list(reversed(new))
        result = json.dumps(new)
        await self.redis.set('message_list', result)

        return message_instance

