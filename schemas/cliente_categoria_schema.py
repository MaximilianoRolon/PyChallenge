from pydantic import BaseModel


class ClienteCategoria(BaseModel):
    cliente_id: str
    categoria_id: str

    class Config:
        orm_mode = True


class ClienteCategoriaOut(BaseModel):
    id: int
    cliente_id: int
    categoria_id: int

    class Config:
        orm_mode = True
