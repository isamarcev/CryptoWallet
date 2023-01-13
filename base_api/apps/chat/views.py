from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from base_api.apps.chat.dependencies import get_db
from base_api.apps.chat.schemas import MessageCreate

chat_router = APIRouter()


@chat_router.post('/message_make')
async def make_message(message: MessageCreate, db: Session = Depends(get_db)):
    pass