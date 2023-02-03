# -*- coding: utf-8 -*-
import json
from datetime import datetime

from aioredis import Redis
from sqlalchemy import asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from base_api.apps.chat.models import Message
from base_api.apps.chat.models import message as message_table
from base_api.apps.chat.schemas import MessageCreate, MessageDetail, MessageDetail1
from base_api.apps.users.models import User
from base_api.apps.users.models import user as user_table


class ChatDatabase:
    """
    :param message_model: message_model

    """

    def __init__(self, message_model: Message, redis: Redis):
        self.message_model = message_model
        self.redis = redis

    async def create_message(self, message: MessageCreate, db: AsyncSession, user: User):
        message_instance = Message(**message.dict(), user_id=user.id, datetime=datetime.now())
        db.add(message_instance)
        await db.commit()
        result = await db.execute(
            select(Message).order_by(message_table.c.datetime.desc()).options(selectinload(Message.user_model)).limit(10)
        )

        result = result.scalars().all()


        new = []
        for message in result:
            message = MessageDetail1(
                text=message.text,
                image=message.image,
                user_id=message.user_id,
                datetime=message.datetime,
                id=message.id,
                user_photo=message.user_model.photo
            )

            new.append(json.loads(message.json()))
        new = list(reversed(new))
        result = json.dumps(new)
        print(type(result))
        await self.redis.set("message_list", result)

        return message_instance
