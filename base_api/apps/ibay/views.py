from typing import List
from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from base_api.apps.ibay.dependencies import get_session, get_ibay_manager
from base_api.apps.ibay.manager import IbayManager
from base_api.apps.ibay.schemas import CreateProduct, Products, CreateOrder, Orders
from base_api.apps.users.dependencies import get_current_user
from base_api.apps.users.models import User
from base_api.config.utils.fastapi_limiter import custom_callback

ibay_router = APIRouter()


@ibay_router.post("/create_product",
                  dependencies=[Depends(RateLimiter(times=2, seconds=10, callback=custom_callback))])
async def create_product(
        product: CreateProduct = Depends(CreateProduct.as_form),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_session),
        manager: IbayManager = Depends(get_ibay_manager)

):
    await manager.create_product(product, user, db)
    return status.HTTP_201_CREATED


@ibay_router.post("/create-order",
                  dependencies=[Depends(RateLimiter(times=2, seconds=5, callback=custom_callback))])
async def create_order(
        product: CreateOrder,
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
        ibay_manager: IbayManager = Depends(get_ibay_manager),
):
    await ibay_manager.create_order(user, session, product)
    return status.HTTP_201_CREATED


@ibay_router.get("/products", response_model=List[Products],
                 dependencies=[Depends(RateLimiter(times=3, seconds=5, callback=custom_callback))])
async def get_products(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_session),
        manager: IbayManager = Depends(get_ibay_manager)
):
    response = await manager.get_products(user, db)
    return response


@ibay_router.get("/orders", response_model=List[Orders],
                 dependencies=[Depends(RateLimiter(times=3, seconds=5, callback=custom_callback))])
async def get_orders(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_session),
        ibay_manager: IbayManager = Depends(get_ibay_manager),
):
    response = await ibay_manager.get_user_orders(user, db)
    return response
