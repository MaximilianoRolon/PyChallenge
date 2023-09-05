from fastapi import APIRouter, HTTPException, Depends
from starlette.responses import Response
from starlette.status import HTTP_204_NO_CONTENT
from sqlalchemy.orm import Session
from models import cliente_model, cuenta_model
from schemas import cliente_schema, cuenta_schema, cliente_categoria_schema, movimiento_schema
from crud import crud
from schemas.cliente_schema import Cliente
from config.db import SessionLocal, engine

movimiento = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Registrar un movimiento
@movimiento.post("/movimientos/")
def registrar_movimiento(info_movimiento: movimiento_schema.Movimiento, db: Session = Depends(get_db)):
    return crud.registrar_movimiento(db=db, info_movimiento=info_movimiento)


# Eliminar un movimiento
@movimiento.post("/movimiento/eliminar")
def eliminar_movimiento(info_movimientoId: movimiento_schema.MovimientoId, db: Session = Depends(get_db)):
    return crud.eliminar_movimiento(db=db, info_movimientoId=info_movimientoId)


# Consultar un movimiento
@movimiento.get("/movimientos/{id}")
def consultar_movimiento(id: int, db: Session = Depends(get_db)):
    return crud.consultar_movimiento(db=db, id=id)
