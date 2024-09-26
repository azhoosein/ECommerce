from sqlalchemy import Integer, String, ForeignKey, DateTime, Column
from sqlalchemy.orm import relationship
from ..db.database import Base

class Shipping(Base):
    __tablename__ = 'shipping'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Foreign key to Users
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)

    user = relationship("Users", back_populates="shipping")

