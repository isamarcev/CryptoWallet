import asyncio
from typing import List
import time
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.background import BackgroundTasks

from base_api.apps.chat.dependencies import get_session
from base_api.apps.ethereum.dependencies import get_ethereum_manager
from base_api.apps.ethereum.manager import EthereumManager
from base_api.apps.ethereum.schemas import WalletCreate, WalletDetail, WalletImport, Wallets
from base_api.apps.ethereum.web3_client import EthereumClient
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


@ethereum_router.post('/import_wallet', response_model=WalletDetail)
async def create_wallet(
        wallet: WalletImport,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_session),
        manager: EthereumManager = Depends(get_ethereum_manager)
):
    response = await manager.import_wallet(wallet, user, db)
    return response


@ethereum_router.get('/user_wallets', response_model=List[Wallets])
async def get_user_wallets(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_session),
        manager: EthereumManager = Depends(get_ethereum_manager)
):
    response = await manager.get_user_wallets(user, db)
    return response


@ethereum_router.get('/get_balance')
async def get_balance(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_session),
        manager: EthereumManager = Depends(get_ethereum_manager),
        background_tasks=BackgroundTasks
):
    wallets = ['0x26a3da7DCE53Cbcb0a77Df8A41eC2C59050Cd18c', '0x26a3da7DCE53Cbcb0a77Df8A41eC2C59050Cd18c', '0x26a3da7DCE53Cbcb0a77Df8A41eC2C59050Cd18c']
    client = EthereumClient()
    task = []
    # start = time.time()
    # for wallet in wallets:
    #     task.append(client.sync_get_balance(wallet))
    # # await asyncio.gather(*task)
    # end = time.time() - start  ## собственно время работы программы
    # print('sync = ', end)  ## вывод времени
    start = time.time()
    for _ in range(10):
        task.append(client.get_balance('0x26a3da7DCE53Cbcb0a77Df8A41eC2C59050Cd18c'))
    await asyncio.gather(*task)
    end = time.time() - start  ## собственно время работы программы
    print('async = ', end)  ## вывод времени
    return {'status': 'ok'}


