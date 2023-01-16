from fastapi import APIRouter

from sockets.apps.chat.views import chat_router
from base_api.apps.users.views import user_router

router = APIRouter(
    prefix='/api'
    )


router.include_router(chat_router, prefix='/chat', tags=['Chat'])
router.include_router(user_router, prefix='/user', tags=['User'])
