from sqlmodel import select
from sqlmodel import SQLModel
from typing import Type, TypeVar, Generic, List, Optional
from .db import get_session
T = TypeVar("T", bound=SQLModel)

class CRUD(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    def list(self, skip: int = 0, limit: int = 50) -> List[T]:
        with get_session() as s:
            return list(s.exec(select(self.model).offset(skip).limit(limit)))

    def get(self, id: int) -> Optional[T]:
        with get_session() as s:
            return s.get(self.model, id)

    def create(self, obj: T) -> T:
        with get_session() as s:
            s.add(obj)
            s.commit()
            s.refresh(obj)
            return obj

    def update(self, id: int, data: dict) -> Optional[T]:
        with get_session() as s:
            obj = s.get(self.model, id)
            if not obj: return None
            for k,v in data.items():
                if hasattr(obj, k): setattr(obj, k, v)
            s.add(obj); s.commit(); s.refresh(obj)
            return obj

    def delete(self, id: int) -> bool:
        with get_session() as s:
            obj = s.get(self.model, id)
            if not obj: return False
            s.delete(obj); s.commit()
            return True
