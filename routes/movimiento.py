from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import Response
from starlette.status import HTTP_406_NOT_ACCEPTABLE

from schemas import movimiento_schema
from crud import crud
from config.db import get_db

movimiento = APIRouter()


# Registrar un movimiento
@movimiento.post("/movimientos/", response_model=movimiento_schema.MovimientoOut)
def registrar_movimiento(info_movimiento: movimiento_schema.Movimiento, db: Session = Depends(get_db)):
    response = crud.registrar_movimiento(db=db, info_movimiento=info_movimiento)
    if response == "HTTP_406_NOT_ACCEPTABLE":
        response = Response(status_code=HTTP_406_NOT_ACCEPTABLE)
    return response


# Eliminar un movimiento
@movimiento.post("/movimiento/eliminar", response_model=int)
def eliminar_movimiento(info_movimiento_id: movimiento_schema.MovimientoId, db: Session = Depends(get_db)):
    response = crud.eliminar_movimiento(db=db, info_movimiento_id=info_movimiento_id)
    if response == "HTTP_406_NOT_ACCEPTABLE":
        response = Response(status_code=HTTP_406_NOT_ACCEPTABLE)
    return response


# Consultar un movimiento
@movimiento.get("/movimientos", response_model=movimiento_schema.MovimientoOut)
def consultar_movimiento(movimiento_id: int, db: Session = Depends(get_db)):
    response = crud.consultar_movimiento(db=db, movimiento_id=movimiento_id)
    if response == "HTTP_406_NOT_ACCEPTABLE":
        response = Response(status_code=HTTP_406_NOT_ACCEPTABLE)
    return response
