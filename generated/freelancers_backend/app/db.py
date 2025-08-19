from sqlmodel import SQLModel, create_engine, Session
import os

DB_URL = os.environ.get("DB_URL", "sqlite:///data/app.db")
connect_args = {"check_same_thread": False} if DB_URL.startswith("sqlite") else {}
engine = create_engine(DB_URL, echo=False, connect_args=connect_args)

def init_db():
    from .models import *  # ensure models imported
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)
