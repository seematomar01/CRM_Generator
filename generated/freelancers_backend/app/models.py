from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, datetime


class Client(SQLModel, table=True):
    
    id: int = Field(default=None, primary_key=True)
    
    name: str
    
    email: str
    
    phone: str
    

class Project(SQLModel, table=True):
    
    id: int = Field(default=None, primary_key=True)
    
    client_id: int = Field(foreign_key="clients.id")
    
    name: str
    
    rate_per_hour: float
    

class TimeEntry(SQLModel, table=True):
    
    id: int = Field(default=None, primary_key=True)
    
    project_id: int = Field(foreign_key="projects.id")
    
    hours: float
    
    note: str
    

class Invoice(SQLModel, table=True):
    
    id: int = Field(default=None, primary_key=True)
    
    project_id: int = Field(foreign_key="projects.id")
    
    amount: float
    
    status: str
    
