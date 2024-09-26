from pydantic import BaseModel
from typing import Optional

class productCreate(BaseModel):
    name: str
    description: str
    price: float
    quantity: int

    class Config:
        from_attributes = True
        extra = "forbid"  # Disallow extra fields 

class productRead(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int

    class Config:
        from_attributes = True