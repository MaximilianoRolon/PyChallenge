from pydantic import BaseModel


class Movimiento(BaseModel):
    cuenta_id: int
    tipo: str
    importe: int

    class Config:
        orm_mode = True


class MovimientoId(BaseModel):
    id: str

    class Config:
        orm_mode = True
