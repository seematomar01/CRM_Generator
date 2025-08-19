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

client_crud = CRUD(Client)

@router.get("/clients", response_model=List[Client])
def list_clients(skip: int = 0, limit: int = 50):
    return client_crud.list(skip=skip, limit=limit)

@router.get("/clients/{id}", response_model=Client)
def get_clients(id: int):
    obj = client_crud.get(id)
    if not obj: raise HTTPException(status_code=404, detail="Client not found")
    return obj

@router.post("/clients", response_model=Client)
def create_clients(payload: Client):
    return client_crud.create(payload)

class ClientUpdate(BaseModel):
    
    name: str | None = None
    
    email: str | None = None
    
    phone: str | None = None
    

@router.patch("/clients/{id}", response_model=Client)
def update_clients(id: int, payload: ClientUpdate):
    obj = client_crud.update(id, payload.model_dump(exclude_unset=True))
    if not obj: raise HTTPException(status_code=404, detail="Client not found")
    return obj

@router.delete("/clients/{id}")
def delete_clients(id: int):
    ok = client_crud.delete(id)
    if not ok: raise HTTPException(status_code=404, detail="Client not found")
    return {"ok": True}

project_crud = CRUD(Project)

@router.get("/projects", response_model=List[Project])
def list_projects(skip: int = 0, limit: int = 50):
    return project_crud.list(skip=skip, limit=limit)

@router.get("/projects/{id}", response_model=Project)
def get_projects(id: int):
    obj = project_crud.get(id)
    if not obj: raise HTTPException(status_code=404, detail="Project not found")
    return obj

@router.post("/projects", response_model=Project)
def create_projects(payload: Project):
    return project_crud.create(payload)

class ProjectUpdate(BaseModel):
    
    client_id: int | None = None
    
    name: str | None = None
    
    rate_per_hour: float | None = None
    

@router.patch("/projects/{id}", response_model=Project)
def update_projects(id: int, payload: ProjectUpdate):
    obj = project_crud.update(id, payload.model_dump(exclude_unset=True))
    if not obj: raise HTTPException(status_code=404, detail="Project not found")
    return obj

@router.delete("/projects/{id}")
def delete_projects(id: int):
    ok = project_crud.delete(id)
    if not ok: raise HTTPException(status_code=404, detail="Project not found")
    return {"ok": True}

timeentry_crud = CRUD(TimeEntry)

@router.get("/time_entries", response_model=List[TimeEntry])
def list_time_entries(skip: int = 0, limit: int = 50):
    return timeentry_crud.list(skip=skip, limit=limit)

@router.get("/time_entries/{id}", response_model=TimeEntry)
def get_time_entries(id: int):
    obj = timeentry_crud.get(id)
    if not obj: raise HTTPException(status_code=404, detail="TimeEntry not found")
    return obj

@router.post("/time_entries", response_model=TimeEntry)
def create_time_entries(payload: TimeEntry):
    return timeentry_crud.create(payload)

class TimeEntryUpdate(BaseModel):
    
    project_id: int | None = None
    
    hours: float | None = None
    
    note: str | None = None
    

@router.patch("/time_entries/{id}", response_model=TimeEntry)
def update_time_entries(id: int, payload: TimeEntryUpdate):
    obj = timeentry_crud.update(id, payload.model_dump(exclude_unset=True))
    if not obj: raise HTTPException(status_code=404, detail="TimeEntry not found")
    return obj

@router.delete("/time_entries/{id}")
def delete_time_entries(id: int):
    ok = timeentry_crud.delete(id)
    if not ok: raise HTTPException(status_code=404, detail="TimeEntry not found")
    return {"ok": True}

invoice_crud = CRUD(Invoice)

@router.get("/invoices", response_model=List[Invoice])
def list_invoices(skip: int = 0, limit: int = 50):
    return invoice_crud.list(skip=skip, limit=limit)

@router.get("/invoices/{id}", response_model=Invoice)
def get_invoices(id: int):
    obj = invoice_crud.get(id)
    if not obj: raise HTTPException(status_code=404, detail="Invoice not found")
    return obj

@router.post("/invoices", response_model=Invoice)
def create_invoices(payload: Invoice):
    return invoice_crud.create(payload)

class InvoiceUpdate(BaseModel):
    
    project_id: int | None = None
    
    amount: float | None = None
    
    status: str | None = None
    

@router.patch("/invoices/{id}", response_model=Invoice)
def update_invoices(id: int, payload: InvoiceUpdate):
    obj = invoice_crud.update(id, payload.model_dump(exclude_unset=True))
    if not obj: raise HTTPException(status_code=404, detail="Invoice not found")
    return obj

@router.delete("/invoices/{id}")
def delete_invoices(id: int):
    ok = invoice_crud.delete(id)
    if not ok: raise HTTPException(status_code=404, detail="Invoice not found")
    return {"ok": True}


# ------ Domain Extras ------

class GenerateInvoicePayload(BaseModel):
    project_id: int

@router.post("/invoices/generate", response_model=Invoice)
def generate_invoice(payload: GenerateInvoicePayload):
    with get_session() as s:
        project = s.get(Project, payload.project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        rate = project.rate_per_hour or 0.0
        hours = 0.0
        from sqlmodel import select
        for te in s.exec(select(TimeEntry).where(TimeEntry.project_id == project.id)):
            hours += te.hours or 0.0
        amount = hours * rate
        inv = Invoice(project_id=project.id, amount=amount, status="draft")
        s.add(inv); s.commit(); s.refresh(inv)
        return inv
