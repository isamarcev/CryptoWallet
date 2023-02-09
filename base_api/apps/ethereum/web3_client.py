import asyncio
import concurrent
import functools
from abc import ABC
from web3 import Web3

from base_api.apps.ethereum.exeptions import Web3ConnectionError, TransactionError
from base_api.config.settings import settings


class BaseClient(ABC):

    @property
    def provider(self):
        try:
            provider = Web3(Web3.WebsocketProvider(settings.infura_api_url))
            print(f"Is connected: {provider.isConnected()}")
        except:
            print('888')
            raise Web3ConnectionError()
        return provider


class EthereumClient(BaseClient):

    # async def get_balance(self, address):
    #     print('async get balance')
    #     loop = asyncio.get_running_loop()
    #     balance = await loop.run_in_executor(None, functools.partial(self.sync_get_balance, address=address))
    #     print(balance)
    #     return balance

    def sync_get_balance(self, address: str) -> str:
        checksum_address = Web3.toChecksumAddress(address)
        try:
            balance = self.provider.eth.get_balance(checksum_address)
        except ValueError:
            return self.sync_get_balance(address)
        ether_balance = Web3.fromWei(balance, 'ether')
        return ether_balance

    @staticmethod
    def build_txn(provider: Web3, from_address: str, to_address: str, amount: float):
        gas_price = provider.eth.gas_price
        gas = 21000
        nonce = provider.eth.getTransactionCount(from_address)

        txn = {
            'chainId': provider.eth.chain_id,
            'from': from_address,
            'to': to_address,
            'value': int(Web3.toWei(amount, 'ether')),
            'nonce': nonce,
            'gasPrice': gas_price,
            'gas': gas,
        }
        return txn

    def sync_send_transaction(self, from_address: str, to_address: str, amount: float, private_key: str):
        try:
            provider = self.provider
            transaction = self.build_txn(provider, from_address, to_address, amount)
            signed_txn = provider.eth.account.sign_transaction(transaction, private_key)
            txn_hash = provider.eth.send_raw_transaction(signed_txn.rawTransaction)
            print('success transaction = ', txn_hash.hex())
            return txn_hash.hex()
        except Exception as ex:
            print(ex)
            raise TransactionError(str(ex))

    def sync_get_transaction_receipt(self, txn_hash: str):
        try:
            txn = self.provider.eth.get_transaction_receipt(txn_hash)
            print(txn)
            return txn
        except Exception:
            print('error get transaction_receipt')
