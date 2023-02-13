from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from base_api.apps.ibay.dependencies import get_session, get_ibay_manager
from base_api.apps.ibay.manager import IbayManager
from base_api.apps.ibay.schemas import CreateProduct, ProductInfo, Products
from base_api.apps.users.dependencies import get_current_user
from base_api.apps.users.models import User

ibay_router = APIRouter()


@ibay_router.post("/create_product", response_model=ProductInfo)
async def create_product(
        product: CreateProduct = Depends(CreateProduct.as_form),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_session),
        manager: IbayManager = Depends(get_ibay_manager)

):
    response = await manager.create_product(product, user, db)
    return response


@ibay_router.get("/products", response_model=List[Products])
async def create_product(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_session),
        manager: IbayManager = Depends(get_ibay_manager)
):
    response = await manager.get_products(user, db)
    return response
