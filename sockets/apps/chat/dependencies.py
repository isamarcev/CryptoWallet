from async_lru import alru_cache
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from sockets.apps.chat.database import ChatDatabase
from sockets.apps.chat.manager import ChatManager
from sockets.apps.chat.models import Message
from base_api.config.db import async_session


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


@alru_cache()
async def get_chat_db() -> ChatDatabase:
    return ChatDatabase(Message)


@alru_cache()
async def get_chat_manager() -> ChatManager:
    chat_db = await get_chat_db()
    return ChatManager(chat_db)


#test get current_user
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

#take user by token


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     user = await users_utils.get_user_by_token(token)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     if not user["is_active"]:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
#         )
#     return user