from sqlalchemy.ext.asyncio import AsyncSession

from base_api.apps.ethereum.models import Wallet
from base_api.apps.ethereum.schemas import WalletCreate


class EthereumDatabase:
    def __init__(self, wallet_model: Wallet):
        self.wallet_model = wallet_model

    async def add_wallet(self, wallet: WalletCreate, db: AsyncSession):
        wallet_instance = self.wallet_model(**wallet.dict(), currency_type='token', currency_name='ethereum')
        db.add(wallet_instance)
        await db.commit()
        return wallet_instance
