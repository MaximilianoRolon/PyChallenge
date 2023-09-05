from typing import Optional
from pydantic import BaseModel


class Movimiento(BaseModel):
        id: Optional[str] = None
        cuenta_id: int
        tipo: str
        importe: int
        fecha: Optional[str] = None
        class Config:
                orm_mode = True
