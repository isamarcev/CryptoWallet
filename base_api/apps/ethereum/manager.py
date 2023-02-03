import secrets

from sqlalchemy.ext.asyncio import AsyncSession
from eth_account import Account
from base_api.apps.ethereum.database import EthereumDatabase
from base_api.apps.ethereum.schemas import WalletCreate
from base_api.apps.users.models import User


class EthereumManager:
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
        except Exception as ex:
            #TODO: make exeption
            pass
        return await self.database.add_wallet(wallet, db)


