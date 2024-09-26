from fastapi import Depends, HTTPException, status, APIRouter, Response
from typing import List
from sqlalchemy.orm import Session
from ..db.database import getDB
from ..auth.oauth2 import getCurrentUser, getCurrentAdmin
from ..models import order as orderModel
from ..models import product as productModel
from ..schemas import order as orderSchemas
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(
    prefix="/api/order",
    tags=["order"]
)

# OAuth2 scheme for admin authentication (if required)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.get("/")
def getUserOrders(db: Session = Depends(getDB), userId: int = Depends(getCurrentUser)):
    orders = db.query(orderModel.Orders).filter(orderModel.Orders.user_id == userId.id).all()
    return {"data": orders}

@router.post("/", status_code=status.HTTP_201_CREATED)
def createOrder(order: orderSchemas.orderCreate, db: Session = Depends(getDB), userId: int = Depends(getCurrentUser)):
    products = db.query(productModel.Products).filter(productModel.Products.id.in_(order.product_ids)).all()
    
    if len(products) != len(order.product_ids):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="One or more products not found.")

    total_price = sum(product.price for product in products)

    new_order = orderModel.Orders(user_id=userId.id, total_price=total_price)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for product in products:
        new_order_product = orderModel.order_product_association.insert().values(order_id=new_order.id, product_id=product.id, quantity=1)
        db.execute(new_order_product)

    db.commit()
    
    return {"message": "Order created successfully", "order_id": new_order.id}

@router.get("/{id}")
def getOrderById(id: int, db: Session = Depends(getDB), userId: int = Depends(getCurrentUser)):
    order = db.query(orderModel.Orders).filter(orderModel.Orders.id == id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id: {id} does not exist!")
    if order.user_id != userId.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized.")
    return {"data": order}

@router.put("/{id}")
def updateOrder(id: int, order: orderSchemas.orderCreate, db: Session = Depends(getDB), userId: int = Depends(getCurrentUser)):
    order_in_db = db.query(orderModel.Orders).filter(orderModel.Orders.id == id).first()
    if not order_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found.")
    if order_in_db.user_id != userId.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized.")
    
    # Update order logic can go here (e.g., changing products)
    # You can implement your business logic for updating an order

    db.commit()
    return {"message": "Order updated successfully", "order": order_in_db}

@router.delete("/{id}")
def deleteOrder(id: int, db: Session = Depends(getDB), userId: int = Depends(getCurrentUser)):
    order_in_db = db.query(orderModel.Orders).filter(orderModel.Orders.id == id).first()
    if not order_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found.")
    if order_in_db.user_id != userId.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized.")
    
    db.delete(order_in_db)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/admin")
def getAllOrders(db: Session = Depends(getDB), current_admin: bool = Depends(getCurrentAdmin)):
    orders = db.query(orderModel.Orders).all()
    return {"data": orders}
