import uuid as uuid_id

from sqlalchemy import Column, String, ForeignKey, Float, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
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
    balance = Column(Float)
    user = Column(ForeignKey(User.id))

    transactions = relationship('Transaction', back_populates='wallet')


wallet = Wallet.__table__


class Transaction(Base):
    STATUS = [
        ('Success', 'Success'),
        ('Pending', 'Pending'),
        ('Failed', 'Failed')
    ]
    __tablename__ = 'transaction'

    id: UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid_id.uuid4)
    number = Column(String)
    from_address = Column(String)
    to_address = Column(String)
    value = Column(String)
    date = Column(DateTime(timezone=True), server_default=func.now())
    txn_fee = Column(String)
    status = Column(ChoiceType(STATUS), nullable=False)
    wallet_id = Column('wallet_id', ForeignKey(Wallet.id))

    wallet = relationship(Wallet, back_populates='transactions')
