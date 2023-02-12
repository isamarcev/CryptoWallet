# -*- coding: utf-8 -*-
from typing import Dict

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from base_api.apps.ibay.database import IbayDatabase
from base_api.apps.users.schemas import UserLogin, UserProfileUpdate, UserRegister

from ...config.storage import Storage


class IbayManager:
    def __init__(
        self,
        database: IbayDatabase,
        storage: Storage
    ):
        self.database = database
        self.storage = storage


