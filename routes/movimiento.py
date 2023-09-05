from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import movimiento_schema
from crud import crud
from config.db import SessionLocal

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
def eliminar_movimiento(info_movimiento_id: movimiento_schema.MovimientoId, db: Session = Depends(get_db)):
    return crud.eliminar_movimiento(db=db, info_movimiento_id=info_movimiento_id)


# Consultar un movimiento
@movimiento.get("/movimientos")
def consultar_movimiento(movimiento_id: int, db: Session = Depends(get_db)):
    return crud.consultar_movimiento(db=db, movimiento_id=movimiento_id)
