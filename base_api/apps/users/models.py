import uuid

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import EmailType, URLType
import uuid as uuid_id
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def get_new_uuid():
    return str(uuid_id.uuid4())


class Permission(Base):
    __tablename__ = 'permissions'
    id: int = Column(Integer, primary_key=True)
    has_chat_access = Column(Boolean)

perm = Permission.__table__


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    photo = Column(URLType)
    email = Column(EmailType)
    password = Column(String)
    permission = relationship("Permission", backref="users", uselist=False)
    message = relationship("..chat.models.Message", backref="users")


user = User.__table__