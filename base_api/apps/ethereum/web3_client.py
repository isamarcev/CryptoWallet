import asyncio
import concurrent
import functools
from abc import ABC
from web3 import Web3

from base_api.config.settings import settings


class BaseClient(ABC):

    @property
    def provider(self):
        provider = Web3(Web3.WebsocketProvider(settings.infura_api_url))
        print(f"Is connected: {provider.isConnected()}")
        return provider


class EthereumClient(BaseClient):

    async def get_balance(self, address):
        print('async get balance')
        loop = asyncio.get_running_loop()
        balance = await loop.run_in_executor(None, functools.partial(self.sync_get_balance, address=address))
        print(balance)
        return balance

    def sync_get_balance(self, address: str) -> dict:
        checksum_address = Web3.toChecksumAddress(address)
        try:
            balance = self.provider.eth.get_balance(checksum_address)
        except ValueError:
            return self.sync_get_balance(address)
        ether_balance = Web3.fromWei(balance, 'ether')  # Decimal('1')
        print(f"balance of {address}={ether_balance} Wei")
        return {"address": address, "balance": balance}

