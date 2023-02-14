import uuid
import uuid as uuid_id

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, func, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType, URLType

from base_api.apps.ethereum.models import Wallet
from base_api.apps.ibay.enums import OrderStatus

Base = declarative_base()


class Product(Base):
    __tablename__ = "product"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    price = Column(Float)
    address = Column('wallet_id', ForeignKey(Wallet.id))
    image = Column(URLType)
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    order = relationship("Order", backref="product", uselist=False)
    is_sold = Column(Boolean, default=False)
    wallet = relationship(Wallet, backref='product')


product = Product.__table__


class Order(Base):
    __tablename__ = "order"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    txn_hash = Column(String)
    datetime = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(Enum(OrderStatus), default=OrderStatus.NEW)
    txn_hash_return = Column(String, nullable=True)
    buyer_wallet = Column(String)
    product_id = Column(UUID(as_uuid=True), ForeignKey(Product.id))


order = Order.__table__
