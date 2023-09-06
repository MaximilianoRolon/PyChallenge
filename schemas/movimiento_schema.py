import decimal

from pydantic import BaseModel

from data_type.enums import TipoEnum


class Movimiento(BaseModel):
    cuenta_id: int
    tipo: TipoEnum
    importe: decimal.Decimal

    class Config:
        orm_mode = True


class MovimientoId(BaseModel):
    id: str

    class Config:
        orm_mode = True


class MovimientoOut(BaseModel):
    id: int
    cuenta_id: int
    tipo: TipoEnum
    importe: decimal.Decimal
    fecha: str

    class Config:
        orm_mode = True
