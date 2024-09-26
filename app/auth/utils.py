from passlib.context import CryptContext
from ..db.database import getDB
from  sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from ..models.product import Products as productsModel

pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashPwd(pwd : str) -> str:
    return pwdContext.hash(pwd)

def verifyPwd(pwd: str, hashedPwd: str) -> bool:
    return pwdContext.verify(pwd, hashedPwd)    

def checkOwner(productId: int, userId: int, db: Session = Depends(getDB)):
    product = db.query(productsModel.Products).filter(productsModel.Products.id == productId)
    if not product.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id: {productId} does not exist!")
    if product.first().user_id != userId:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized.")
    return product