from pydantic import BaseModel


class Cuenta(BaseModel):
    cliente_id: str

    class Config:
        orm_mode = True


class CuentaOut(BaseModel):
    cliente_id: int

    class Config:
        orm_mode = True
