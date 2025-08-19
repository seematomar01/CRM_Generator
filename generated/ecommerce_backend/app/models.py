from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, datetime


class Customer(SQLModel, table=True):
    
    id: int = Field(default=None, primary_key=True)
    
    name: str
    
    email: str
    
    phone: str
    

class Product(SQLModel, table=True):
    
    id: int = Field(default=None, primary_key=True)
    
    name: str
    
    price: float
    
    stock: int
    

class Order(SQLModel, table=True):
    
    id: int = Field(default=None, primary_key=True)
    
    customer_id: int = Field(foreign_key="customers.id")
    
    product_id: int = Field(foreign_key="products.id")
    
    quantity: int
    
    total: float | None = None
    
