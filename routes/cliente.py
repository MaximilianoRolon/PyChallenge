from fastapi import APIRouter, HTTPException, Depends
from starlette.responses import Response
from starlette.status import HTTP_204_NO_CONTENT
from sqlalchemy.orm import Session
from models import cliente_model, cuenta_model
from schemas import cliente_schema, cuenta_schema, cliente_categoria_schema
from crud import crud
from schemas.cliente_schema import Cliente
from config.db import SessionLocal, engine

cliente = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Consultar cuentas y categorias de un cliente
@cliente.get("/clientes/{id}")
def consultar_cuentas_y_categorias(id: int, db: Session = Depends(get_db)):
    return crud.consultar_cuentas_y_categorias(db=db, id=id)


# Registrar un cliente
@cliente.post("/clientes/")
def registrar_cliente(cliente: cliente_schema.Cliente, db: Session = Depends(get_db)):
    return crud.registrar_cliente(db=db, info_cliente=cliente)


# Editar un cliente
@cliente.post("/cliente/edit")
def editar_cliente(cliente: cliente_schema.ClienteEdit, db: Session = Depends(get_db)):
    return crud.editar_cliente(db=db, info_cliente=cliente)


# Listar clientes
@cliente.get("/clientes")
def listar_clientes(db: Session = Depends(get_db)):
    result = crud.listar_clientes(db)
    return result



# Eliminar clientes
@cliente.post("/cliente/eliminar")
def eliminar_cliente(info_clienteId: cliente_schema.ClienteId, db: Session = Depends(get_db)):
    return crud.eliminar_cliente(db=db, info_clienteId=info_clienteId)


# Añadir cliente a categoria
@cliente.post("/cliente/categoria")
def añadir_cliente_a_categoria(info_cliente_categoria: cliente_categoria_schema.ClienteCategoria, db: Session = Depends(get_db)):
    return crud.añadir_cliente_a_categoria(db=db, info_cliente_categoria=info_cliente_categoria)



# Consultar saldo en cuentas
@cliente.get("/clientes/saldo/{id}")
def consultar_saldo(id: int, db: Session = Depends(get_db)):
    return crud.consultar_saldo(db=db, id=id)



# Consultar saldo en cuentas en dolares
@cliente.get("/clientes/saldo/dolar/{id}")
def consultar_saldo(id: int, db: Session = Depends(get_db)):
    return crud.consultar_saldo(db=db, id=id, dolar=True)

