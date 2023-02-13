import json

from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from base_api.apps.frontend.dependecies import check_user_token
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession

from base_api.apps.ibay.dependencies import get_session, get_ibay_manager
from base_api.apps.ibay.manager import IbayManager

from base_api.apps.ibay.scheme import CreateOrder
from base_api.apps.users.dependencies import get_current_user
from base_api.apps.users.models import User


ibay_router = APIRouter()


@ibay_router.get("/products",
                  status_code=status.HTTP_201_CREATED)
async def create_product(
        session: AsyncSession = Depends(get_session),
        ibay_manager: IbayManager = Depends(get_ibay_manager)

):
    data = [{"title": "Teddy Bear", "image": "fasdfasdf", "address": "01212122xx fasdfsd", "price": 3},
            {"title": "Teddy Bear2", "image": "fasdfasdf2222", "address": "22222222222 fasdfsd", "price": 3}]
    return data


@ibay_router.post("/create-order")
async def create_order(
        product: CreateOrder,
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
        ibay_manager: IbayManager = Depends(get_ibay_manager),
):
    if not user:
        raise HTTPException(status_code=403, detail="You don't have permission")
    response = await ibay_manager.create_order(user, session, product)
    return response

