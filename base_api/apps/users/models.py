# -*- coding: utf-8 -*-
import uuid
from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType


Base = declarative_base()


class Permission(Base):
    __tablename__ = "permissions"
    id: int = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    has_chat_access = Column(Boolean, default=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))



perm = Permission.__table__


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    photo = Column(URLType)
    email = Column(String)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    permission = relationship(Permission, backref="users", uselist=False)


user = User.__table__
