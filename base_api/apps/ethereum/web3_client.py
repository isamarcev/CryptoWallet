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

    async def get_balance(self, address: str):
        print('async')
        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor() as new_pool:
            balance = await loop.run_in_executor(new_pool, functools.partial(self.sync_get_balance, address=address))
        return balance

    def sync_get_balance(self, address: str):
        checksum_address = Web3.toChecksumAddress(address)
        balance = self.provider.eth.get_balance(checksum_address)
        ether_balance = Web3.fromWei(balance, 'ether')  # Decimal('1')
        print(f"balance of {address}={ether_balance} Wei")
        return balance

