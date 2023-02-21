from fastapi import APIRouter

from base_api.apps.frontend.auth import auth_router
from base_api.apps.frontend.chat import chat_router
from base_api.apps.frontend.ibay import front_ibay_router
from base_api.apps.frontend.user_profile import profile_router
from base_api.apps.frontend.wallets import wallets_router

front_router = APIRouter()

front_router.include_router(auth_router)
front_router.include_router(profile_router)
front_router.include_router(chat_router)
front_router.include_router(wallets_router)
front_router.include_router(front_ibay_router)
