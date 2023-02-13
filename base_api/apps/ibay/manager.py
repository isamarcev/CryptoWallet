# -*- coding: utf-8 -*-
import datetime
from typing import Dict

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from base_api.apps.ibay.database import IbayDatabase
from base_api.apps.ibay.scheme import CreateOrder
from ...base_api_producer import BaseApiProducer

from ...config.storage import Storage


class IbayManager:
    def __init__(
        self,
        database: IbayDatabase,
        # storage: Storage,
        producer: BaseApiProducer,
    ):
        self.database = database
        # self.storage = storage
        self.producer = producer

    async def create_order(self, user, db, product: CreateOrder):
        # create transaction
        txn_hash = "qwerty"
        #write data to DB - >
        data = {
            "product_id": str(product.product),
            "txn_hash": txn_hash,
            "buyer_wallet": product.from_wallet,
        }

        order = await self.database.create_order(data, db)

        message = order

        await self.producer.publish_message(
            "new_order",
            message=message,
        )
        print("MESSEGE SENT")

        return {"Good": "FOOD"}


