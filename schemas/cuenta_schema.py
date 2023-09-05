from typing import Optional
from pydantic import BaseModel


class Cuenta(BaseModel):
        id: Optional[str] = None
        cliente_id: str
        class Config:
                orm_mode = True
