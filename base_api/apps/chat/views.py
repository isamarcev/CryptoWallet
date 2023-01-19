from fastapi import APIRouter, Depends
from fastapi_helper.authorization.cookies_jwt_http_bearer import auth_bearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from base_api.apps.chat.dependencies import get_session, get_chat_manager
from base_api.apps.chat.manager import ChatManager
from base_api.apps.chat.schemas import MessageCreate
from base_api.apps.users.dependencies import get_current_user
from base_api.apps.users.models import User

chat_router = APIRouter()


@chat_router.post('/chat/message_create')
async def create_message(
        request: Request,
        token: str = Depends(auth_bearer),
        user: User = Depends(get_current_user),
        message: MessageCreate = Depends(MessageCreate.as_form),
        db: AsyncSession = Depends(get_session),
        message_manager: ChatManager = Depends(get_chat_manager)):
    response = await message_manager.create_message(message, db)
    print('token = ', request.cookies.get("Authorization"))
    print('tokenq = ', token)
    return response
