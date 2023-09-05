from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import cliente_schema, cliente_categoria_schema
from crud import crud
from config.db import SessionLocal

cliente = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Consultar cuentas y categorias de un cliente
@cliente.get("/clientes/info")
def consultar_cuentas_y_categorias(cliente_id: int, db: Session = Depends(get_db)):
    return crud.consultar_cuentas_y_categorias(db=db, cliente_id=cliente_id)


# Registrar un cliente
@cliente.post("/clientes")
def registrar_cliente(info_cliente: cliente_schema.Cliente, db: Session = Depends(get_db)):
    return crud.registrar_cliente(db=db, info_cliente=info_cliente)


# Editar un cliente
@cliente.post("/cliente/edit")
def editar_cliente(info_cliente: cliente_schema.ClienteEdit, db: Session = Depends(get_db)):
    return crud.editar_cliente(db=db, info_cliente=info_cliente)


# Listar clientes
@cliente.get("/clientes")
def listar_clientes(db: Session = Depends(get_db)):
    result = crud.listar_clientes(db)
    return result


# Eliminar clientes
@cliente.post("/cliente/eliminar")
def eliminar_cliente(info_cliente_id: cliente_schema.ClienteId, db: Session = Depends(get_db)):
    return crud.eliminar_cliente(db=db, info_cliente_id=info_cliente_id)


# Añadir cliente a categoria
@cliente.post("/cliente/categoria")
def añadir_cliente_a_categoria(info_cliente_categoria: cliente_categoria_schema.ClienteCategoria,
                               db: Session = Depends(get_db)):
    return crud.añadir_cliente_a_categoria(db=db, info_cliente_categoria=info_cliente_categoria)


# Consultar saldo en cuentas
@cliente.get("/clientes/saldo")
def consultar_saldo(cliente_id: int, db: Session = Depends(get_db)):
    return crud.consultar_saldo(db=db, cliente_id=cliente_id)


# Consultar saldo en cuentas en dolares
@cliente.get("/clientes/saldo/dolar")
def consultar_saldo(cliente_id: int, db: Session = Depends(get_db)):
    return crud.consultar_saldo(db=db, cliente_id=cliente_id, dolar=True)
