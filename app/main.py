from fastapi import FastAPI
from .db.database import engine
from .routes import product, user, order
from .models import product as productsModel
from .models import user as userModel
from .models import order as orderModel
from .models import shipping as shippingModel

productsModel.Base.metadata.create_all(bind=engine)
userModel.Base.metadata.create_all(bind=engine)
orderModel.Base.metadata.create_all(bind=engine)
shippingModel.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(product.router)
app.include_router(user.router)
app.include_router(order.router)
