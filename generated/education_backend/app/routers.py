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

student_crud = CRUD(Student)

@router.get("/students", response_model=List[Student])
def list_students(skip: int = 0, limit: int = 50):
    return student_crud.list(skip=skip, limit=limit)

@router.get("/students/{id}", response_model=Student)
def get_students(id: int):
    obj = student_crud.get(id)
    if not obj: raise HTTPException(status_code=404, detail="Student not found")
    return obj

@router.post("/students", response_model=Student)
def create_students(payload: Student):
    return student_crud.create(payload)

class StudentUpdate(BaseModel):
    
    name: str | None = None
    
    email: str | None = None
    

@router.patch("/students/{id}", response_model=Student)
def update_students(id: int, payload: StudentUpdate):
    obj = student_crud.update(id, payload.model_dump(exclude_unset=True))
    if not obj: raise HTTPException(status_code=404, detail="Student not found")
    return obj

@router.delete("/students/{id}")
def delete_students(id: int):
    ok = student_crud.delete(id)
    if not ok: raise HTTPException(status_code=404, detail="Student not found")
    return {"ok": True}

course_crud = CRUD(Course)

@router.get("/courses", response_model=List[Course])
def list_courses(skip: int = 0, limit: int = 50):
    return course_crud.list(skip=skip, limit=limit)

@router.get("/courses/{id}", response_model=Course)
def get_courses(id: int):
    obj = course_crud.get(id)
    if not obj: raise HTTPException(status_code=404, detail="Course not found")
    return obj

@router.post("/courses", response_model=Course)
def create_courses(payload: Course):
    return course_crud.create(payload)

class CourseUpdate(BaseModel):
    
    title: str | None = None
    
    code: str | None = None
    

@router.patch("/courses/{id}", response_model=Course)
def update_courses(id: int, payload: CourseUpdate):
    obj = course_crud.update(id, payload.model_dump(exclude_unset=True))
    if not obj: raise HTTPException(status_code=404, detail="Course not found")
    return obj

@router.delete("/courses/{id}")
def delete_courses(id: int):
    ok = course_crud.delete(id)
    if not ok: raise HTTPException(status_code=404, detail="Course not found")
    return {"ok": True}

admission_crud = CRUD(Admission)

@router.get("/admissions", response_model=List[Admission])
def list_admissions(skip: int = 0, limit: int = 50):
    return admission_crud.list(skip=skip, limit=limit)

@router.get("/admissions/{id}", response_model=Admission)
def get_admissions(id: int):
    obj = admission_crud.get(id)
    if not obj: raise HTTPException(status_code=404, detail="Admission not found")
    return obj

@router.post("/admissions", response_model=Admission)
def create_admissions(payload: Admission):
    return admission_crud.create(payload)

class AdmissionUpdate(BaseModel):
    
    student_id: int | None = None
    
    course_id: int | None = None
    
    status: str | None = None
    

@router.patch("/admissions/{id}", response_model=Admission)
def update_admissions(id: int, payload: AdmissionUpdate):
    obj = admission_crud.update(id, payload.model_dump(exclude_unset=True))
    if not obj: raise HTTPException(status_code=404, detail="Admission not found")
    return obj

@router.delete("/admissions/{id}")
def delete_admissions(id: int):
    ok = admission_crud.delete(id)
    if not ok: raise HTTPException(status_code=404, detail="Admission not found")
    return {"ok": True}


# ------ Domain Extras ------

class EnrollPayload(BaseModel):
    student_id: int
    course_id: int

@router.post("/admissions/enroll", response_model=Admission)
def enroll_student(payload: EnrollPayload):
    with get_session() as s:
        st = s.get(Student, payload.student_id)
        cr = s.get(Course, payload.course_id)
        if not st or not cr:
            raise HTTPException(status_code=400, detail="Invalid student or course")
        adm = Admission(student_id=payload.student_id, course_id=payload.course_id, status="enrolled")
        s.add(adm); s.commit(); s.refresh(adm)
        return adm

