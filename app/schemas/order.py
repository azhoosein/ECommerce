from pydantic import BaseModel
from typing import List

class orderRead(BaseModel):
    id: int
    class Config:
        from_attributes = True

class orderCreate(BaseModel):
    product_ids: List[int]  # List of product IDs to include in the order
