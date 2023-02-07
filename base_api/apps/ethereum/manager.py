import asyncio
import functools
import secrets
from abc import ABC, abstractmethod
from eth_keys import keys
from eth_utils import decode_hex
from sqlalchemy.ext.asyncio import AsyncSession
from eth_account import Account
from base_api.apps.ethereum.database import EthereumDatabase
from base_api.apps.ethereum.exeptions import WalletCreatingError, InvalidWalletImport, WalletAlreadyExists, \
    WalletIsNotDefine
from base_api.apps.ethereum.schemas import WalletCreate, WalletImport, CreateTransaction
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
    def __init__(self, database: EthereumDatabase, client: EthereumClient):
        self.database = database
        self.client = client

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
        balance = await self.get_wallet_balance(public_key)
        wallet = WalletCreate(user=user.id, privet_key=privet_key, public_key=public_key, balance=balance)
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
        return await self.database.get_user_wallets(user, db)

    async def get_wallet_balance(self, wallet: str):
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, functools.partial(self.client.sync_get_balance, address=wallet))
        return result

    async def send_transaction(self, transaction: CreateTransaction, user: User, db: AsyncSession):
        wallet_user = self.database.get_wallet_by_public_key(transaction.from_address, db)
        if not wallet_user or wallet_user.user != user.id:
            raise WalletIsNotDefine()
        #TODO: check balance and transaction value

        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, functools.partial(self.client.sync_send_transaction,
                                                                    from_address='0x26a3da7DCE53Cbcb0a77Df8A41eC2C59050Cd18c',
                                                                    to_address='0xbB940f3198fDD455AaF8B4e5C7bbd2D5067A9c35',
                                                                    amount=0.4,
                                                                    private_key='2f3e90ea508dd911ee318114e89894da9e62318d4073c2dd7dc0823c6e72baff'))




