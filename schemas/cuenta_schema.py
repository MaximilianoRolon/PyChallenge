from typing import Optional
from pydantic import BaseModel


class Cuenta(BaseModel):
        cliente_id: str
        class Config:
                orm_mode = True
