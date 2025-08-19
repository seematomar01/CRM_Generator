from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, datetime


class Patient(SQLModel, table=True):
    
    id: int = Field(default=None, primary_key=True)
    
    name: str
    
    dob: date
    
    gender: str
    
    email: str
    
    phone: str
    

class Doctor(SQLModel, table=True):
    
    id: int = Field(default=None, primary_key=True)
    
    name: str
    
    specialty: str
    
    email: str
    
    phone: str
    

class Appointment(SQLModel, table=True):
    
    id: int = Field(default=None, primary_key=True)
    
    patient_id: int = Field(foreign_key="patients.id")
    
    doctor_id: int = Field(foreign_key="doctors.id")
    
    scheduled_for: datetime
    
    notes: str
    
