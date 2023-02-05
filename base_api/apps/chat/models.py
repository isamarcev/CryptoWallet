# -*- coding: utf-8 -*-
import uuid as uuid_id

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, MetaData, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy_utils import EmailType, URLType

from base_api.apps.users.models import User

Base = declarative_base()


class Chat(Base):
    __tablename__ = "chats"
    id: UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid_id.uuid4)


chat = Chat.__table__


class Message(Base):
    __tablename__ = "messages"

    id: UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid_id.uuid4)
    user_id = Column("user_id", ForeignKey(User.id))
    text = Column(String)
    image = Column(URLType)
    datetime = Column(DateTime(timezone=True), server_default=func.now())

    user_model = relationship(User, backref='messages')


message = Message.__table__
