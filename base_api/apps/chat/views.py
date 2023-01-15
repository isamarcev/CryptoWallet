from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from base_api.apps.chat.dependencies import get_session, get_chat_manager
from base_api.apps.chat.manager import ChatManager
from base_api.apps.chat.schemas import MessageCreate


chat_router = APIRouter()


@chat_router.post('/chat/message_create')
async def create_message(
        message: MessageCreate,
        db: AsyncSession = Depends(get_session),
        message_manager: ChatManager = Depends(get_chat_manager)):
    response = await message_manager.create_message(message, db)
    return response
