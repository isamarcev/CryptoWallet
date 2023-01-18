from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from sockets.apps.chat.mongo_models import ChatUser, Message
from sockets.config.settings import settings

client = AsyncIOMotorClient(str(settings.mongodb_url))


async def init_mongo():
    await init_beanie(database=client[settings.mongo_name],
                      document_models=[Message, ChatUser])
