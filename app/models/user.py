from sqlalchemy import String, Integer, DateTime, Column, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..db.database import Base

class Users(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_admin = Column(Boolean, default=False)  # Added field to indicate admin status

    # Relationships
    products = relationship("Products", back_populates="user")
    orders = relationship("Orders", back_populates="user")
    reviews = relationship("ProductReviews", back_populates="user")
    shipping = relationship("Shipping", back_populates="user")  # Add this line


    