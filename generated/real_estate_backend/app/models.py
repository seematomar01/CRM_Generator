from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, datetime


class Property(SQLModel, table=True):
    
    id: int = Field(default=None, primary_key=True)
    
    address: str
    
    city: str
    
    price: float
    
    status: str
    

class Agent(SQLModel, table=True):
    
    id: int = Field(default=None, primary_key=True)
    
    name: str
    
    email: str
    
    phone: str
    

class Lead(SQLModel, table=True):
    
    id: int = Field(default=None, primary_key=True)
    
    name: str
    
    email: str
    
    phone: str
    
    interested_property_id: int = Field(foreign_key="properties.id")
    
    assigned_agent_id: int = Field(foreign_key="agents.id")
    
