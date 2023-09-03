from typing import Optional
from pydantic import BaseModel


class Cliente(BaseModel):
        id: Optional[str] = None
        nombre: str
