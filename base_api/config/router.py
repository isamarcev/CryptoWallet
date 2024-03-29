# -*- coding: utf-8 -*-
from fastapi import APIRouter

from base_api.apps.chat.views import chat_router
from base_api.apps.ethereum.views import ethereum_router
from base_api.apps.ibay.views import ibay_router
from base_api.apps.users.views import user_router

router = APIRouter(
    prefix="/api",
)


router.include_router(chat_router, prefix="/chat", tags=["Chat"])
router.include_router(user_router, prefix="/user", tags=["User"])
router.include_router(ethereum_router, prefix='/wallet', tags=['Wallet'])
router.include_router(ibay_router, prefix='/ibay', tags=['Ibay'])
