from typing import Optional
from pydantic import BaseModel


class ClienteCategoria(BaseModel):
        cliente_id: str
        categoria_id: str
        class Config:
                orm_mode = True
