import asyncio
import functools
import json
import secrets
import socketio

from abc import ABC, abstractmethod
from datetime import datetime

from eth_keys import keys
from eth_utils import decode_hex
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from eth_account import Account
from web3 import Web3
from aioredis import Redis


from base_api.apps.ethereum.database import EthereumDatabase
from base_api.apps.ethereum.exeptions import WalletCreatingError, InvalidWalletImport, WalletAlreadyExists, \
    WalletIsNotDefine
from base_api.apps.ethereum.schemas import WalletCreate, WalletImport, CreateTransaction, CreateTransactionReceipt, \
    TransactionURL
from base_api.apps.ethereum.web3_client import EthereumClient
from base_api.apps.users.models import User
from base_api.config.settings import settings


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
    def __init__(self, database: EthereumDatabase, client: EthereumClient, redis: Redis):
        self.database = database
        self.client = client
        self.redis = redis

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
        wallet = WalletCreate(user=user.id, privet_key=privet_key, public_key=public_key)
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
        wallets = await self.database.get_user_wallets(user, db)
        if wallets:
            loop = asyncio.get_running_loop()
            result = [loop.run_in_executor(None, functools.partial(self.client.sync_get_balance, address=wallet.public_key))
                      for wallet in wallets]
            balances = await asyncio.gather(*result, return_exceptions=False)
            for number, wallet in enumerate(wallets):
                wallet.balance = balances[number]
        return wallets

    async def get_wallet_balance(self, wallet: str):
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, functools.partial(self.client.sync_get_balance, address=wallet))
        return result

    async def send_transaction(self, transaction: CreateTransaction, user: User, db: AsyncSession):
        user_wallet = await self.database.get_wallet_by_public_key(transaction.from_address, db)
        if not user_wallet or user_wallet.user != user.id:
            raise WalletIsNotDefine()
        if not Web3.isAddress(transaction.to_address):
            raise WalletIsNotDefine(message='Wallet address is not defined')
        loop = asyncio.get_running_loop()
        txn_hash = await loop.run_in_executor(None, functools.partial(self.client.sync_send_transaction,
                                                                      from_address=transaction.from_address,
                                                                      to_address=transaction.to_address,
                                                                      amount=transaction.amount,
                                                                      private_key=user_wallet.privet_key))
        transaction_receipt = CreateTransactionReceipt(
            number=txn_hash,
            from_address=transaction.from_address,
            to_address=transaction.to_address,
            value=transaction.amount,
            date=datetime.now(),
            txn_fee=None,
            status='Pending'
        )
        new_transaction_receipt = await self.database.create_transaction(transaction_receipt, db)
        tracking_transaction = await self.redis.get('transaction')
        if tracking_transaction:
            tracking_transaction.append(txn_hash)
        else:
            tracking_transaction = [txn_hash]
        await self.redis.set("transaction", json.dumps(tracking_transaction))
        return TransactionURL(url='https://sepolia.etherscan.io/tx/' + txn_hash)

    async def check_transaction_in_block(self, block_number, db: AsyncSession):
        wallets = await self.database.get_wallets(db)
        addresses = [wallet.public_key for wallet in wallets]
        print(addresses, "ADDREDDSE")
        loop = asyncio.get_event_loop()
        transactions = await loop.run_in_executor(None, functools.partial(self.client.get_transaction_by_block,
                                                                        block_number=block_number,
                                                                        addresses=addresses))
        if transactions:
            socket_manager = socketio.AsyncAioPikaManager(settings.rabbit_url)
            users_online = await self.redis.get("users_online")
            # try:
            users = json.loads(users_online)
            # except:
            #     pass
            for transaction in transactions:
                txn_hash = transaction.hash
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(None, functools.partial(self.client.sync_get_transaction_receipt,
                                                                            txn_hash=txn_hash,
                                                                            ))

                if transaction['to'] in addresses:
                    wallet_owner = await self.database.get_wallet_by_public_key(transaction["to"], db)
                    current_balance = await loop.run_in_executor(None, functools.partial(self.client.sync_get_balance,
                                                                            address=transaction["to"],
                                                                            ))
                    print(current_balance, "CURRENT BALANCE")
                    message = {
                        "operation": "income",
                        "result": True if result.get("status") else False,
                        "public_key": transaction["to"],
                        "current_balance": current_balance,
                    }
                    await socket_manager.emit("transaction_alert", data=message, to=users.get(wallet_owner.user.id))

                elif transaction["from"] in addresses:
                    address = transaction["from"]
                    wallet_owner = await self.database.get_wallet_by_public_key(transaction["from"], db)
                    current_balance = await loop.run_in_executor(None, functools.partial(self.client.sync_get_balance,
                                                                                         address=address,
                                                                                         ))
                    print(current_balance, "CURRENT BALANCE")
                    message = {
                        "operation": "outcome",
                        "result": True if result.get("status") else False,
                        "public_key": address,
                        "current_balance": current_balance,
                    }
                    await socket_manager.emit("transaction_alert", data=message, to=users.get(wallet_owner.user.id))
        message = {
            "operation": "outcome",
            "BLOCK": block_number
        }
        socket_manager = socketio.AsyncAioPikaManager(settings.rabbit_url)
        users_online = await self.redis.get("users_online")
        # try:
        print(users_online)
        users = json.loads(users_online)
        print(users.get("40bf9645-6847-4fcc-a04e-ef63a0feb9c2"), "SID")
        nonTrue = users.get("40bf9645-6847-4fcc-a04e-ef63a0feb9c2", "1")
        TrueTrue = users.get("40bf9645-6847-4fcc-a04e-ef63a0feb9c3", "1")
        print(users.get("40bf9645-6847-4fcc-a04e-ef63a0feb9c3"), "SID")
        await socket_manager.emit("transaction_alert",
                                  data=message,
                                  room=TrueTrue)


            # хочет ли фронтенд обновлять данные на следующую страницу по скроллу
            # если хочет получить оффсет и лимит , нам нужно это учесть.
            # Короткое кеширование - на 5 секунд. в редисе.

            # ЕСЛИ ТРАНЗАЦИЯ ЕСТЬ В ОЖИДАНИЯХ - ШЛЮ ЗАПРОС В БД на ИЗМЕНЕНИЯ ЕЕ СТАТУСА, и НА ФРОНТ ОПОВЕЩАНИЯ
            # ЕСЛИ НЕТ В ОЖИДАНИИ, СОЗДАЮ ТРАНЗАКЦИЮ В БД И ШЛЮ ЮЗЕРУ О ЗАХОДЕ ДЕНЕГ

        # нужно получить статус этой транзакции с апи
        #


        print("CELERY CHECKER")
        return



