from pydantic import BaseModel


class Categoria(BaseModel):
    nombre: str

    class Config:
        orm_mode = True


class CategoriaOut(BaseModel):
    id: int
    nombre: str

    class Config:
        orm_mode = True
