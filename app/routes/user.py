from fastapi import Depends, status, HTTPException, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..schemas.user import UserCreate, UserRead, UserLogin, Token
from ..db.database import getDB
from sqlalchemy.orm import Session
from ..auth import utils, oauth2
from ..models.user import Users as userModel

router = APIRouter(
    prefix='/api',  # Removed unnecessary parentheses
    tags=['users']
)

@router.post('/login', response_model=Token)
def login(userLogin: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(getDB)):
    # Fetch user by username
    user = db.query(userModel).filter(userModel.username == userLogin.username).first()
    
    # Validate user existence
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username does not exist!")
    
    # Validate password
    if not utils.verifyPwd(userLogin.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials!")
    
    # Create token with user ID and admin status
    token_data = {"userId": user.id, "is_admin": user.is_admin}  # Assuming user model has is_admin attribute
    token = oauth2.createToken(data=token_data)

    return {"access_token": token, "token_type": "bearer"}

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserRead)
def createUser(user: UserCreate, db: Session = Depends(getDB)):
    # Check for existing email
    if db.query(userModel).filter(userModel.email == user.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists!")
    
    # Check for existing username
    if db.query(userModel).filter(userModel.username == user.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists!")
    
    # Hash password and create user
    hashedPassword = utils.hashPwd(user.password)
    user.password = hashedPassword
    newUser = userModel(**user.dict())  # Directly set the hashed password
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    
    return newUser
