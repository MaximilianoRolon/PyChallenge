from typing import Optional
from pydantic import BaseModel


class Cliente(BaseModel):
        nombre: str
        class Config:
                orm_mode = True

class ClienteEdit(BaseModel):
        id: str
        nombre: str
        class Config:
                orm_mode = True

class ClienteId(BaseModel):
        id: str
        class Config:
                orm_mode = True
