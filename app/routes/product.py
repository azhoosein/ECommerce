from fastapi import Depends, Response, status, HTTPException, APIRouter
from typing import List
from ..schemas.product import productCreate, productRead
from ..db.database import getDB
from sqlalchemy.orm import Session
from ..models import product as productsModel
from ..auth.oauth2 import getCurrentUser
from ..auth.utils import checkOwner

router = APIRouter(
    prefix="/api/products",
    tags=['products']
)

@router.get("/", response_model=List[productRead])
def getProducts(db: Session = Depends(getDB)):
    products = db.query(productsModel.Products).all()
    return products

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=productRead)
def createProduct(product: productCreate, db: Session = Depends(getDB), userId: int = Depends(getCurrentUser)):
    newProduct = productsModel.Products(**product.dict(), user_id=userId.id)
    db.add(newProduct)
    db.commit()
    db.refresh(newProduct)
    return newProduct

@router.get("/{id}", response_model=productRead)
def getProductById(id: int, db: Session = Depends(getDB)):
    product = db.query(productsModel.Products).filter(productsModel.Products.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id: {id} does not exist!")
    return product

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteProduct(id: int, db: Session = Depends(getDB), userId: int = Depends(getCurrentUser)):
    productInDb = checkOwner(id, userId.id, db)
    db.delete(productInDb)  # Corrected method to delete the product instance
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=productRead)
def updateProduct(id: int, product: productCreate, db: Session = Depends(getDB), userId: int = Depends(getCurrentUser)):
    productInDb = checkOwner(id, userId.id, db)
    for key, value in product.dict().items():  # Update only the fields provided in the request
        setattr(productInDb, key, value)
    db.commit()
    return productInDb  # Return the updated product
