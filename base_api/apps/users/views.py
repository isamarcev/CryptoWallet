from sqlalchemy.orm import Session

from dependencies import get_db
from models import User
from fastapi import APIRouter, Depends
import database

user_router = APIRouter()


@user_router.post('/register/{name}')
async def register(
        name: str,
        db: Session = Depends(get_db)
):
    user = await database.UserDatabase.create_user(username=name, db=db)
    return {"user": user}