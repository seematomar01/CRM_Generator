from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from .crud import CRUD
from .models import *
from .db import init_db, get_session

router = APIRouter()

# Initialize DB at import
init_db()

# ------ Generic CRUD Routes ------

customer_crud = CRUD(Customer)

@router.get("/customers", response_model=List[Customer])
def list_customers(skip: int = 0, limit: int = 50):
    return customer_crud.list(skip=skip, limit=limit)

@router.get("/customers/{id}", response_model=Customer)
def get_customers(id: int):
    obj = customer_crud.get(id)
    if not obj: raise HTTPException(status_code=404, detail="Customer not found")
    return obj

@router.post("/customers", response_model=Customer)
def create_customers(payload: Customer):
    return customer_crud.create(payload)

class CustomerUpdate(BaseModel):
    
    name: str | None = None
    
    email: str | None = None
    
    phone: str | None = None
    

@router.patch("/customers/{id}", response_model=Customer)
def update_customers(id: int, payload: CustomerUpdate):
    obj = customer_crud.update(id, payload.model_dump(exclude_unset=True))
    if not obj: raise HTTPException(status_code=404, detail="Customer not found")
    return obj

@router.delete("/customers/{id}")
def delete_customers(id: int):
    ok = customer_crud.delete(id)
    if not ok: raise HTTPException(status_code=404, detail="Customer not found")
    return {"ok": True}

product_crud = CRUD(Product)

@router.get("/products", response_model=List[Product])
def list_products(skip: int = 0, limit: int = 50):
    return product_crud.list(skip=skip, limit=limit)

@router.get("/products/{id}", response_model=Product)
def get_products(id: int):
    obj = product_crud.get(id)
    if not obj: raise HTTPException(status_code=404, detail="Product not found")
    return obj

@router.post("/products", response_model=Product)
def create_products(payload: Product):
    return product_crud.create(payload)

class ProductUpdate(BaseModel):
    
    name: str | None = None
    
    price: float | None = None
    
    stock: int | None = None
    

@router.patch("/products/{id}", response_model=Product)
def update_products(id: int, payload: ProductUpdate):
    obj = product_crud.update(id, payload.model_dump(exclude_unset=True))
    if not obj: raise HTTPException(status_code=404, detail="Product not found")
    return obj

@router.delete("/products/{id}")
def delete_products(id: int):
    ok = product_crud.delete(id)
    if not ok: raise HTTPException(status_code=404, detail="Product not found")
    return {"ok": True}

order_crud = CRUD(Order)

@router.get("/orders", response_model=List[Order])
def list_orders(skip: int = 0, limit: int = 50):
    return order_crud.list(skip=skip, limit=limit)

@router.get("/orders/{id}", response_model=Order)
def get_orders(id: int):
    obj = order_crud.get(id)
    if not obj: raise HTTPException(status_code=404, detail="Order not found")
    return obj

@router.post("/orders", response_model=Order)
def create_orders(payload: Order):
    return order_crud.create(payload)

class OrderUpdate(BaseModel):
    
    customer_id: int | None = None
    
    product_id: int | None = None
    
    quantity: int | None = None
    
    total: float | None = None
    

@router.patch("/orders/{id}", response_model=Order)
def update_orders(id: int, payload: OrderUpdate):
    obj = order_crud.update(id, payload.model_dump(exclude_unset=True))
    if not obj: raise HTTPException(status_code=404, detail="Order not found")
    return obj

@router.delete("/orders/{id}")
def delete_orders(id: int):
    ok = order_crud.delete(id)
    if not ok: raise HTTPException(status_code=404, detail="Order not found")
    return {"ok": True}


# ------ Domain Extras ------

@router.post("/orders/{order_id}/compute-total", response_model=Order)
def compute_order_total(order_id: int):
    with get_session() as s:
        order = s.get(Order, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        product = s.get(Product, order.product_id)
        if not product:
            raise HTTPException(status_code=400, detail="Invalid product")
        order.total = (order.quantity or 0) * (product.price or 0.0)
        s.add(order); s.commit(); s.refresh(order)
        return order

