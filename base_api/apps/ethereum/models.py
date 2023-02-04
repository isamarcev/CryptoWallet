import uuid as uuid_id

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import ChoiceType

from base_api.apps.users.models import User

Base = declarative_base()


class Wallet(Base):
    TYPES = [
        ('token', 'token'),
        ('coin', 'coin')
    ]
    __tablename__ = "wallet"

    id: UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid_id.uuid4)
    currency_type = Column(ChoiceType(TYPES), nullable=False)
    currency_name = Column(String)
    public_key = Column(String, unique=True)
    privet_key = Column(String, unique=True)
    user = Column(ForeignKey(User.id))


wallet = Wallet.__table__

