# models/product.py
from sqlalchemy import String, Float, Integer, ForeignKey, Column
from sqlalchemy.orm import relationship
from ..db.database import Base


class Products(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    user = relationship("Users", back_populates="products")
    reviews = relationship("ProductReviews", back_populates="product")
    categories = relationship("ProductCategories", back_populates="product")


# models/review.py
class ProductReviews(Base):
    __tablename__ = 'product_reviews'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    review_text = Column(String, nullable=False)

    # Relationships
    product = relationship("Products", back_populates="reviews")
    user = relationship("Users", back_populates="reviews")

# models/category.py
class ProductCategories(Base):
    __tablename__ = 'product_categories'
    
    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'), primary_key=True)

    # Relationships
    product = relationship("Products", back_populates="categories")
    category = relationship("Categories", back_populates="products")

class Categories(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)

    # Relationships
    products = relationship("ProductCategories", back_populates="category")

