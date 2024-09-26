from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True
        extra = "forbid"


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True
        extra = "forbid"

class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        extra = "forbid"

class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        extra = "forbid"

class TokenData(BaseModel):
    id: int
    is_admin: Optional[bool] = False  # Default to False if not provided

    class Config:
        extra = "forbid"
