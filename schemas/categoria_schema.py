from typing import Optional
from pydantic import BaseModel


class Categoria(BaseModel):
        id: Optional[str] = None
        nombre: str
        class Config:
                orm_mode = True
