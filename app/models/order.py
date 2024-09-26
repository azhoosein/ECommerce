from sqlalchemy import Integer, Float, ForeignKey, DateTime, Column, Table, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..db.database import Base


# Association table for orders and products
order_product_association = Table(
    'order_product_association', Base.metadata,
    Column('order_id', ForeignKey('orders.id'), primary_key=True),
    Column('product_id', ForeignKey('products.id'), primary_key=True),
    Column('quantity', Integer, nullable=False)  # Add quantity for each product in the order
)

class Orders(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_price = Column(Float, nullable=False)
    order_status = Column(String, nullable=False, default="processing")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("Users", back_populates="orders")


