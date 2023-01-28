# -*- coding: utf-8 -*-
from aioredis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from base_api.apps.chat.database import ChatDatabase
from base_api.apps.chat.schemas import MessageCreate
from base_api.apps.users.models import User
from base_api.base_api_producer import BaseApiProducer


class ChatManager:
    def __init__(self, database: ChatDatabase, producer: BaseApiProducer):
        self.database = database
        self.producer = producer

    async def create_message(self, message: MessageCreate, db: AsyncSession, user: User):
        created_message = await self.database.create_message(message, db, user)
        message = {
            "user_id": str(created_message.user),
            "text": created_message.text,
            "image": created_message.image,
        }
        await self.producer.publish_message(exchange_name="new_message", message=message)
        return created_message
