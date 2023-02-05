import asyncio
import secrets
from abc import ABC, abstractmethod

from eth_keys import keys
import codecs

from eth_utils import decode_hex
from sqlalchemy.ext.asyncio import AsyncSession
from eth_account import Account
from base_api.apps.ethereum.database import EthereumDatabase
from base_api.apps.ethereum.exeptions import WalletCreatingError, InvalidWalletImport, WalletAlreadyExists
from base_api.apps.ethereum.schemas import WalletCreate, WalletImport
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
    def __init__(self, database: EthereumDatabase):
        self.database = database

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
            wallet = WalletCreate(user=user.id, privet_key=privet_key, public_key=public_key)
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

    async def get_user_wallets(self, user: User, db: AsyncSession):
        return await self.database.get_user_wallets(user, db)

    async def get_balance(self, user: User, db: AsyncSession):
        wallets = await self.get_user_wallets(user, db)
        if wallets:
            client = EthereumClient()
            result = [client.get_balance(wallet.public_key) for wallet in wallets]
            balances = await asyncio.gather(*result, return_exceptions=True)
            print(result, "RESULT GET BALANCE")
            print(balances, "BALANCES")
            for i in balances:
                print(type(i))
            return balances
        return {}






