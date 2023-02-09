import asyncio
import functools
import json
import secrets
from abc import ABC, abstractmethod
from datetime import datetime

from aioredis import Redis
from eth_keys import keys
from eth_utils import decode_hex
from sqlalchemy.ext.asyncio import AsyncSession
from eth_account import Account
from web3 import Web3

from base_api.apps.ethereum.database import EthereumDatabase
from base_api.apps.ethereum.exeptions import WalletCreatingError, InvalidWalletImport, WalletAlreadyExists, \
    WalletIsNotDefine
from base_api.apps.ethereum.schemas import WalletCreate, WalletImport, CreateTransaction, CreateTransactionReceipt, \
    TransactionURL
from base_api.apps.ethereum.web3_client import EthereumClient
from base_api.apps.users.models import User


class BaseManager(ABC):

    @abstractmethod
    async def create_new_wallet(self, user, db):
        pass

    @abstractmethod
    async def import_wallet(self, wallet, user, db):
        pass


class EthereumLikeManager(BaseManager):

    @staticmethod
    @abstractmethod
    async def create_privet_key():
        pass


class EthereumManager(EthereumLikeManager):
    def __init__(self, database: EthereumDatabase, client: EthereumClient, redis: Redis):
        self.database = database
        self.client = client
        self.redis = redis

    @staticmethod
    async def create_privet_key():
        privet_token = secrets.token_hex(32)
        private_key = "0x" + privet_token
        return private_key

    async def create_new_wallet(self, user: User, db: AsyncSession):
        privet_key = await self.create_privet_key()
        try:
            account = Account.from_key(privet_key)
            public_key = account.address
            wallet = WalletCreate(user=user.id, privet_key=privet_key, public_key=public_key, balance=0)
        except Exception:
            raise WalletCreatingError()
        return await self.database.add_wallet(wallet, db)

    async def import_wallet(self, wallet: WalletImport, user: User, db: AsyncSession):
        privet_key = wallet.privet_key
        try:
            pri_key = decode_hex(privet_key)
            pk = keys.PrivateKey(pri_key)
            pub_key = pk.public_key
            public_key = pub_key.to_checksum_address()
        except Exception:
            raise InvalidWalletImport()
        if await self.database.get_wallet_by_public_key(public_key, db):
            raise WalletAlreadyExists()
        wallet = WalletCreate(user=user.id, privet_key=privet_key, public_key=public_key)
        return await self.database.add_wallet(wallet, db)

    # async def get_balance(self, wallets: List[Wallet]):
    #     if wallets:
    #         client = EthereumClient()
    #         loop = asyncio.get_running_loop()
    #         result = [loop.run_in_executor(None, functools.partial(client.sync_get_balance, address=wallet.public_key)) for wallet in wallets]
    #         balances = await asyncio.gather(*result, return_exceptions=True)
    #         print('balances = ', balances)
    #         return balances
    #     return {}

    async def get_user_wallets(self, user: User, db: AsyncSession):
        wallets = await self.database.get_user_wallets(user, db)
        if wallets:
            loop = asyncio.get_running_loop()
            result = [loop.run_in_executor(None, functools.partial(self.client.sync_get_balance, address=wallet.public_key))
                      for wallet in wallets]
            balances = await asyncio.gather(*result, return_exceptions=False)
            for number, wallet in enumerate(wallets):
                wallet.balance = balances[number]
        return wallets

    async def get_wallet_balance(self, wallet: str):
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, functools.partial(self.client.sync_get_balance, address=wallet))
        return result

    async def send_transaction(self, transaction: CreateTransaction, user: User, db: AsyncSession):
        user_wallet = await self.database.get_wallet_by_public_key(transaction.from_address, db)
        if not user_wallet or user_wallet.user != user.id:
            raise WalletIsNotDefine()
        if not Web3.isAddress(transaction.to_address):
            raise WalletIsNotDefine(message='Wallet address is not defined')
        loop = asyncio.get_running_loop()
        txn_hash = await loop.run_in_executor(None, functools.partial(self.client.sync_send_transaction,
                                                                      from_address=transaction.from_address,
                                                                      to_address=transaction.to_address,
                                                                      amount=transaction.amount,
                                                                      private_key=user_wallet.privet_key))
        transaction_receipt = CreateTransactionReceipt(
            number=txn_hash,
            from_address=transaction.from_address,
            to_address=transaction.to_address,
            value=transaction.amount,
            date=datetime.now(),
            txn_fee=None,
            status='Pending'
        )
        new_transaction_receipt = await self.database.create_transaction(transaction_receipt, db)
        tracking_transaction = await self.redis.get('transaction')
        if tracking_transaction:
            tracking_transaction.append(txn_hash)
        else:
            tracking_transaction = [txn_hash]
        await self.redis.set("transaction", json.dumps(tracking_transaction))
        return TransactionURL(url='https://sepolia.etherscan.io/tx/' + txn_hash)



