from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import EmailType, URLType
from sqlalchemy.sql import func
import uuid as uuid_id
from sqlalchemy.ext.declarative import declarative_base
from ..users.models import User


Base = declarative_base()


def get_new_uuid():
    return str(uuid_id.uuid4())


class Chat(Base):
    __tablename__ = 'chats'
    id: UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid_id.uuid4)


chat = Chat.__table__


class Message(Base):
    __tablename__ = "messages"

    id: UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid_id.uuid4)
    user = Column('user_id', ForeignKey(User.id))
    text = Column(String)
    image = Column(URLType)
    datetime = Column(DateTime(timezone=True), server_default=func.now())


message = Message.__table__