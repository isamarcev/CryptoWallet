from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from base_api.apps.chat.dependencies import get_session
from base_api.apps.ethereum.dependencies import get_ethereum_manager
from base_api.apps.ethereum.manager import EthereumManager
from base_api.apps.ethereum.schemas import WalletCreate, WalletDetail
from base_api.apps.users.dependencies import get_current_user
from base_api.apps.users.models import User

ethereum_router = APIRouter()


@ethereum_router.post("/create_new_wallet", response_model=WalletDetail)
async def create_wallet(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_session),
        manager: EthereumManager = Depends(get_ethereum_manager)
):
    response = await manager.create_new_wallet(user, db)
    return response
