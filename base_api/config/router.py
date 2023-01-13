from fastapi import APIRouter

from base_api.apps.chat.views import chat_router

router = APIRouter(
    prefix='/api',
    tags=['apps']
    )


router.include_router(chat_router, prefix='/chat', tags=['Chat'])
