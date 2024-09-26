from sqlalchemy import Integer, ForeignKey, String, Text, DateTime, Column
from sqlalchemy.sql import func
from ..db.database import Base
from sqlalchemy.orm import relationship


class ProductReviews(Base):
    __tablename__ = 'product_reviews'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    rating = Column(Integer)  # e.g., 1 to 5
    comment = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    product = relationship("Products", back_populates="reviews")
    user = relationship("Users", back_populates="reviews")
