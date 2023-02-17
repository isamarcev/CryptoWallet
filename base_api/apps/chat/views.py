# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession
from base_api.apps.chat.dependencies import get_chat_manager, get_redis, get_session
from base_api.apps.chat.exeptions import MessageForbidden
from base_api.apps.chat.manager import ChatManager
from base_api.apps.chat.schemas import MessageCreate, MessageDetail
from base_api.apps.users.dependencies import get_current_user
from base_api.apps.users.models import User
from base_api.config.utils.fastapi_limiter import custom_callback

chat_router = APIRouter()


@chat_router.post("/message_create", response_model=MessageDetail,
                  dependencies=[Depends(RateLimiter(times=3, seconds=5, callback=custom_callback))])
async def create_message(
    user: User = Depends(get_current_user),
    message: MessageCreate = Depends(MessageCreate.as_form),
    db: AsyncSession = Depends(get_session),
    message_manager: ChatManager = Depends(get_chat_manager),
):
    if not user.permission.has_chat_access:
        raise MessageForbidden()
    response = await message_manager.create_message(message, db, user)
    return response
