from sqlalchemy import Integer, Float, ForeignKey, DateTime, Column, String
from sqlalchemy.sql import func
from ..db.database import Base


class Payments(Base):
    __tablename__ = 'payments'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    payment_method = Column(String, nullable=False)  # e.g., credit card, PayPal
    amount = Column(Float, nullable=False)
    status = Column(String)  # e.g., pending, completed, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
