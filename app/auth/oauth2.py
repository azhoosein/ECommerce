from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from ..schemas.user import TokenData
from dotenv import load_dotenv
import os

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGO = os.getenv("ALGO")
EXPIRE = 30  # Token expiration time in minutes

def createToken(data: dict, token_type: str = "Bearer") -> str:
    newData = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRE)
    newData.update({"exp": expire, "type": token_type})
    # Include admin status in the token
    if "is_admin" in data:
        newData["is_admin"] = data["is_admin"]
    encoded_jwt = jwt.encode(newData, SECRET_KEY, algorithm=ALGO)
    return encoded_jwt

def verifyToken(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGO])
        userId = payload.get("userId")
        is_admin = payload.get("is_admin", False)  # Default to False if not set
        if userId is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )
        token_data = TokenData(id=userId, is_admin=is_admin)  # Assuming TokenData has is_admin attribute
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return token_data

def getCurrentUser(token: str = Depends(oauth2_scheme)) -> TokenData:
    return verifyToken(token)

def getCurrentAdmin(current_user: TokenData = Depends(getCurrentUser)) -> TokenData:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have admin privileges"
        )
    return current_user
