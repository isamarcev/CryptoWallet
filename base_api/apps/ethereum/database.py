from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from base_api.apps.ethereum.models import Wallet, wallet as wallet_table, Transaction
from base_api.apps.ethereum.schemas import WalletCreate, CreateTransactionReceipt
from base_api.apps.users.models import User


class EthereumDatabase:
    def __init__(self, wallet_model: Type[Wallet], transaction_model: Type[Transaction]):
        self.wallet_model = wallet_model
        self.transaction_model = transaction_model

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

    async def create_transaction(self, transaction: CreateTransactionReceipt, db: AsyncSession):
        transaction_instance = self.transaction_model(**transaction.dict())
        db.add(transaction_instance)
        await db.commit()
        return transaction_instance

    async def get_wallets(self, engine) -> list:
        # async with engine.connect() as conn:
        # async with engine
        result = await engine.execute(select(wallet_table))
        # result = await db.execute(
        #     select(self.wallet_model)
        # )
        result_scalar = result.all()
        print(result_scalar, "RESULT SCALAR")
        return result_scalar
