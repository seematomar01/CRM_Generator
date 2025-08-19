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

patient_crud = CRUD(Patient)

@router.get("/patients", response_model=List[Patient])
def list_patients(skip: int = 0, limit: int = 50):
    return patient_crud.list(skip=skip, limit=limit)

@router.get("/patients/{id}", response_model=Patient)
def get_patients(id: int):
    obj = patient_crud.get(id)
    if not obj: raise HTTPException(status_code=404, detail="Patient not found")
    return obj

@router.post("/patients", response_model=Patient)
def create_patients(payload: Patient):
    return patient_crud.create(payload)

class PatientUpdate(BaseModel):
    
    name: str | None = None
    
    dob: date | None = None
    
    gender: str | None = None
    
    email: str | None = None
    
    phone: str | None = None
    

@router.patch("/patients/{id}", response_model=Patient)
def update_patients(id: int, payload: PatientUpdate):
    obj = patient_crud.update(id, payload.model_dump(exclude_unset=True))
    if not obj: raise HTTPException(status_code=404, detail="Patient not found")
    return obj

@router.delete("/patients/{id}")
def delete_patients(id: int):
    ok = patient_crud.delete(id)
    if not ok: raise HTTPException(status_code=404, detail="Patient not found")
    return {"ok": True}

doctor_crud = CRUD(Doctor)

@router.get("/doctors", response_model=List[Doctor])
def list_doctors(skip: int = 0, limit: int = 50):
    return doctor_crud.list(skip=skip, limit=limit)

@router.get("/doctors/{id}", response_model=Doctor)
def get_doctors(id: int):
    obj = doctor_crud.get(id)
    if not obj: raise HTTPException(status_code=404, detail="Doctor not found")
    return obj

@router.post("/doctors", response_model=Doctor)
def create_doctors(payload: Doctor):
    return doctor_crud.create(payload)

class DoctorUpdate(BaseModel):
    
    name: str | None = None
    
    specialty: str | None = None
    
    email: str | None = None
    
    phone: str | None = None
    

@router.patch("/doctors/{id}", response_model=Doctor)
def update_doctors(id: int, payload: DoctorUpdate):
    obj = doctor_crud.update(id, payload.model_dump(exclude_unset=True))
    if not obj: raise HTTPException(status_code=404, detail="Doctor not found")
    return obj

@router.delete("/doctors/{id}")
def delete_doctors(id: int):
    ok = doctor_crud.delete(id)
    if not ok: raise HTTPException(status_code=404, detail="Doctor not found")
    return {"ok": True}

appointment_crud = CRUD(Appointment)

@router.get("/appointments", response_model=List[Appointment])
def list_appointments(skip: int = 0, limit: int = 50):
    return appointment_crud.list(skip=skip, limit=limit)

@router.get("/appointments/{id}", response_model=Appointment)
def get_appointments(id: int):
    obj = appointment_crud.get(id)
    if not obj: raise HTTPException(status_code=404, detail="Appointment not found")
    return obj

@router.post("/appointments", response_model=Appointment)
def create_appointments(payload: Appointment):
    return appointment_crud.create(payload)

class AppointmentUpdate(BaseModel):
    
    patient_id: int | None = None
    
    doctor_id: int | None = None
    
    scheduled_for: datetime | None = None
    
    notes: str | None = None
    

@router.patch("/appointments/{id}", response_model=Appointment)
def update_appointments(id: int, payload: AppointmentUpdate):
    obj = appointment_crud.update(id, payload.model_dump(exclude_unset=True))
    if not obj: raise HTTPException(status_code=404, detail="Appointment not found")
    return obj

@router.delete("/appointments/{id}")
def delete_appointments(id: int):
    ok = appointment_crud.delete(id)
    if not ok: raise HTTPException(status_code=404, detail="Appointment not found")
    return {"ok": True}


# ------ Domain Extras ------

class SchedulePayload(BaseModel):
    patient_id: int
    doctor_id: int
    scheduled_for: datetime
    notes: str | None = None

@router.post("/appointments/schedule", response_model=Appointment)
def schedule_appointment(payload: SchedulePayload):
    with get_session() as s:
        pat = s.get(Patient, payload.patient_id)
        doc = s.get(Doctor, payload.doctor_id)
        if not pat or not doc:
            raise HTTPException(status_code=400, detail="Invalid patient or doctor")
        ap = Appointment(patient_id=payload.patient_id, doctor_id=payload.doctor_id,
                         scheduled_for=payload.scheduled_for, notes=payload.notes or "")
        s.add(ap); s.commit(); s.refresh(ap)
        return ap

