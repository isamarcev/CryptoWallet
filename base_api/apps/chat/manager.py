import socketio
from sqlalchemy.ext.asyncio import AsyncSession
from base_api.apps.chat.database import ChatDatabase
from base_api.apps.chat.schemas import MessageCreate
from base_api.apps.users.models import User
from base_api.base_api_producer import BaseApiProducer
from base_api.config.settings import settings
from base_api.config.storage import Storage


class ChatManager:

    def __init__(self, database: ChatDatabase, producer: BaseApiProducer, storage: Storage):

        self.database = database
        self.producer = producer
        self.storage = storage

    async def create_message(self, message: MessageCreate, db: AsyncSession, user: User):
        image = message.image
        if image:
            message.image = await self.storage.upload_image(image, 'chat', [200, 150])
        created_message = await self.database.create_message(message, db, user)
        message = {
            'user_id': str(created_message.user_id),
            'text': created_message.text,
            'image': created_message.image,
            'user_photo': user.photo,
            'username': user.username
        }

        socket_manager = socketio.AsyncAioPikaManager(settings.rabbit_url)
        await socket_manager.emit('new_message', data=message, room='chat')
        return created_message
