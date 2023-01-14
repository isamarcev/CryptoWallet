from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from base_api.apps.users.dependencies import get_db
from base_api.config.db import database
from base_api.apps.users.database import UserDatabase
from ..apps.users.schemas import UserRegister

# import apps.users.views as views
# from ...apps.users import views
# from ..appsapps.users.views import user_router
# from base_api.apps.users.views import user_router


router = APIRouter(
    prefix='/api',
    tags=['apps']
    )


@router.get('/register/{name}')
async def register(
        name: str,
        db: Session = Depends(get_db)
):
    print(name, "NAME")
    user_schema = UserRegister(username=name)
    user = await UserDatabase.create_user(username=name, db=db)
    print(user, "USER")
    return {"user": user}

# router.include_router(user_router, prefix='/user', tags=['User'])