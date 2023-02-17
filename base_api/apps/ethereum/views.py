import time
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession
from base_api.apps.chat.dependencies import get_session
from base_api.apps.ethereum.dependencies import get_ethereum_manager
from base_api.apps.ethereum.manager import EthereumManager
from base_api.apps.ethereum.schemas import WalletDetail, WalletImport, WalletsInfo, CreateTransaction, \
    WalletTransactions, TransactionURL
from base_api.apps.users.dependencies import get_current_user
from base_api.apps.users.models import User
from base_api.config.utils.fastapi_limiter import custom_callback

ethereum_router = APIRouter()


@ethereum_router.post("/create_new_wallet", response_model=WalletDetail,
                      dependencies=[Depends(RateLimiter(times=2, seconds=10, callback=custom_callback))])
async def create_wallet(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
    manager: EthereumManager = Depends(get_ethereum_manager)
):
    response = await manager.create_new_wallet(user, db)
    return response


@ethereum_router.post('/import_wallet', response_model=WalletDetail,
                      dependencies=[Depends(RateLimiter(times=2, seconds=10, callback=custom_callback))])
async def create_wallet(
    wallet: WalletImport,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
    manager: EthereumManager = Depends(get_ethereum_manager)
):
    response = await manager.import_wallet(wallet, user, db)
    return response


@ethereum_router.get('/get_user_wallets', response_model=List[WalletsInfo],
                     dependencies=[Depends(RateLimiter(times=2, seconds=5, callback=custom_callback))])
async def get_user_wallets(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
    manager: EthereumManager = Depends(get_ethereum_manager)
):
    response = await manager.get_user_wallets(user, db)
    return response


@ethereum_router.post('/send_transaction', response_model=TransactionURL,
                      dependencies=[Depends(RateLimiter(times=2, seconds=10, callback=custom_callback))])
async def send_transaction(
    transaction: CreateTransaction,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
    manager: EthereumManager = Depends(get_ethereum_manager)
):
    if not current_user:
        raise HTTPException(status_code=403, detail="You don't have permission")
    response = await manager.send_transaction(transaction, current_user, db)
    return response


@ethereum_router.get('/get_wallet_transactions/{wallet_id}', response_model=List[WalletTransactions],
                     dependencies=[Depends(RateLimiter(times=3, seconds=10, callback=custom_callback))])
async def get_wallet_transaction(
    wallet_id,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
    manager: EthereumManager = Depends(get_ethereum_manager)
):
    response = await manager.get_wallet_transactions(wallet_id, db)
    return response
