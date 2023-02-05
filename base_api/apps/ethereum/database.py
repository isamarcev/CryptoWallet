from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from base_api.apps.ethereum.exeptions import WalletAlreadyExists
from base_api.apps.ethereum.models import Wallet, wallet as wallet_table
from base_api.apps.ethereum.schemas import WalletCreate
from base_api.apps.users.models import User


class EthereumDatabase:
    def __init__(self, wallet_model: Type[Wallet]):
        self.wallet_model = wallet_model

    async def add_wallet(self, wallet: WalletCreate, db: AsyncSession):
        wallet_instance = self.wallet_model(**wallet.dict(), currency_type='token', currency_name='ethereum')
        db.add(wallet_instance)
        await db.commit()
        return wallet_instance

    async def get_wallet_by_public_key(self, public_key: str, db: AsyncSession):
        result = await db.execute(
            wallet_table.select().where(wallet_table.c.public_key == public_key),
        )
        result_data = result.first()
        return None if not result_data else self.wallet_model(**result_data._asdict())

    async def get_user_wallets(self, user: User, db: AsyncSession):
        result = await db.execute(
            select(self.wallet_model).where(wallet_table.c.user == user.id)
        )
        results = result.scalars().all()
        return results


