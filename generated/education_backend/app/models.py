from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, datetime


class Student(SQLModel, table=True):
    
    id: int = Field(default=None, primary_key=True)
    
    name: str
    
    email: str
    

class Course(SQLModel, table=True):
    
    id: int = Field(default=None, primary_key=True)
    
    title: str
    
    code: str
    

class Admission(SQLModel, table=True):
    
    id: int = Field(default=None, primary_key=True)
    
    student_id: int = Field(foreign_key="students.id")
    
    course_id: int = Field(foreign_key="courses.id")
    
    status: str
    
