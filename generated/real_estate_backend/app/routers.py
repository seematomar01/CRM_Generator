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

property_crud = CRUD(Property)

@router.get("/properties", response_model=List[Property])
def list_properties(skip: int = 0, limit: int = 50):
    return property_crud.list(skip=skip, limit=limit)

@router.get("/properties/{id}", response_model=Property)
def get_properties(id: int):
    obj = property_crud.get(id)
    if not obj: raise HTTPException(status_code=404, detail="Property not found")
    return obj

@router.post("/properties", response_model=Property)
def create_properties(payload: Property):
    return property_crud.create(payload)

class PropertyUpdate(BaseModel):
    
    address: str | None = None
    
    city: str | None = None
    
    price: float | None = None
    
    status: str | None = None
    

@router.patch("/properties/{id}", response_model=Property)
def update_properties(id: int, payload: PropertyUpdate):
    obj = property_crud.update(id, payload.model_dump(exclude_unset=True))
    if not obj: raise HTTPException(status_code=404, detail="Property not found")
    return obj

@router.delete("/properties/{id}")
def delete_properties(id: int):
    ok = property_crud.delete(id)
    if not ok: raise HTTPException(status_code=404, detail="Property not found")
    return {"ok": True}

agent_crud = CRUD(Agent)

@router.get("/agents", response_model=List[Agent])
def list_agents(skip: int = 0, limit: int = 50):
    return agent_crud.list(skip=skip, limit=limit)

@router.get("/agents/{id}", response_model=Agent)
def get_agents(id: int):
    obj = agent_crud.get(id)
    if not obj: raise HTTPException(status_code=404, detail="Agent not found")
    return obj

@router.post("/agents", response_model=Agent)
def create_agents(payload: Agent):
    return agent_crud.create(payload)

class AgentUpdate(BaseModel):
    
    name: str | None = None
    
    email: str | None = None
    
    phone: str | None = None
    

@router.patch("/agents/{id}", response_model=Agent)
def update_agents(id: int, payload: AgentUpdate):
    obj = agent_crud.update(id, payload.model_dump(exclude_unset=True))
    if not obj: raise HTTPException(status_code=404, detail="Agent not found")
    return obj

@router.delete("/agents/{id}")
def delete_agents(id: int):
    ok = agent_crud.delete(id)
    if not ok: raise HTTPException(status_code=404, detail="Agent not found")
    return {"ok": True}

lead_crud = CRUD(Lead)

@router.get("/leads", response_model=List[Lead])
def list_leads(skip: int = 0, limit: int = 50):
    return lead_crud.list(skip=skip, limit=limit)

@router.get("/leads/{id}", response_model=Lead)
def get_leads(id: int):
    obj = lead_crud.get(id)
    if not obj: raise HTTPException(status_code=404, detail="Lead not found")
    return obj

@router.post("/leads", response_model=Lead)
def create_leads(payload: Lead):
    return lead_crud.create(payload)

class LeadUpdate(BaseModel):
    
    name: str | None = None
    
    email: str | None = None
    
    phone: str | None = None
    
    interested_property_id: int | None = None
    
    assigned_agent_id: int | None = None
    

@router.patch("/leads/{id}", response_model=Lead)
def update_leads(id: int, payload: LeadUpdate):
    obj = lead_crud.update(id, payload.model_dump(exclude_unset=True))
    if not obj: raise HTTPException(status_code=404, detail="Lead not found")
    return obj

@router.delete("/leads/{id}")
def delete_leads(id: int):
    ok = lead_crud.delete(id)
    if not ok: raise HTTPException(status_code=404, detail="Lead not found")
    return {"ok": True}


# ------ Domain Extras ------

class AssignLeadPayload(BaseModel):
    lead_id: int
    agent_id: int

@router.post("/leads/assign")
def assign_lead(payload: AssignLeadPayload):
    with get_session() as s:
        lead = s.get(Lead, payload.lead_id)
        agent = s.get(Agent, payload.agent_id)
        if not lead or not agent:
            raise HTTPException(status_code=400, detail="Invalid lead or agent")
        lead.assigned_agent_id = payload.agent_id
        s.add(lead); s.commit()
        return {"ok": True, "lead_id": lead.id, "assigned_agent_id": agent.id}

