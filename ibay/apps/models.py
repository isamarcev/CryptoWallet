import uuid
from ibay.apps.enums import OrderStatus
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, DateTime, Enum, func, String

Base = declarative_base()


class Order(Base):
    __tablename__ = "ibay_order"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_number = Column(String)
    datetime = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(Enum(OrderStatus), default=OrderStatus.NEW)


order_table = Order.__table__