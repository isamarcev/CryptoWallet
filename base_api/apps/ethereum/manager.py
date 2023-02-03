import secrets
from eth_keys import keys
import codecs

from eth_utils import decode_hex
from sqlalchemy.ext.asyncio import AsyncSession
from eth_account import Account
from base_api.apps.ethereum.database import EthereumDatabase
from base_api.apps.ethereum.exeptions import WalletCreatingError, InvalidWalletImport
from base_api.apps.ethereum.schemas import WalletCreate, WalletImport
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
            raise WalletCreatingError()
        return await self.database.add_wallet(wallet, db)

    async def import_wallet(self, wallet: WalletImport, user: User, db: AsyncSession):
        privet_key = wallet.privet_key
        try:
            pri_key = decode_hex(privet_key)
            pk = keys.PrivateKey(pri_key)
            pub_key = pk.public_key
            public_key = pub_key.to_checksum_address()
            wallet = WalletCreate(user=user.id, privet_key=privet_key, public_key=public_key)
        except:
            raise InvalidWalletImport()
        return await self.database.add_wallet(wallet, db)








