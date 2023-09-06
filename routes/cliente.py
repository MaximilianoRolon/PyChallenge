from typing import Union, Tuple, List, Dict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import Response
from starlette.status import HTTP_406_NOT_ACCEPTABLE

from schemas import cliente_schema, cliente_categoria_schema, cuenta_schema, categoria_schema
from crud import crud
from config.db import get_db

cliente = APIRouter()


# response_model=Dict[int, float]
# Consultar cuentas y categorias de un cliente
@cliente.get("/clientes/info", response_model=Tuple[List[cuenta_schema.CuentaOut], List[categoria_schema.CategoriaOut]])
def consultar_cuentas_y_categorias(cliente_id: int, db: Session = Depends(get_db)):
    response = crud.consultar_cuentas_y_categorias(db=db, cliente_id=cliente_id)
    if response == "HTTP_406_NOT_ACCEPTABLE":
        response = Response(status_code=HTTP_406_NOT_ACCEPTABLE)
    return response


# Registrar un cliente
@cliente.post("/clientes", response_model=cuenta_schema.CuentaOut)
def registrar_cliente(info_cliente: cliente_schema.Cliente, db: Session = Depends(get_db)):
    return crud.registrar_cliente(db=db, info_cliente=info_cliente)


# Editar un cliente
@cliente.post("/cliente/edit", response_model=cliente_schema.ClienteOut)
def editar_cliente(info_cliente: cliente_schema.ClienteEdit, db: Session = Depends(get_db)):
    response = crud.editar_cliente(db=db, info_cliente=info_cliente)
    if response == "HTTP_406_NOT_ACCEPTABLE":
        response = Response(status_code=HTTP_406_NOT_ACCEPTABLE)
    return response


# Listar clientes
@cliente.get("/clientes", response_model=List[cliente_schema.Cliente])
def listar_clientes(db: Session = Depends(get_db)):
    result = crud.listar_clientes(db)
    return result


# Eliminar clientes
@cliente.post("/cliente/eliminar", response_model=int)
def eliminar_cliente(info_cliente_id: cliente_schema.ClienteId, db: Session = Depends(get_db)):
    response = crud.eliminar_cliente(db=db, info_cliente_id=info_cliente_id)
    if response == "HTTP_406_NOT_ACCEPTABLE":
        response = Response(status_code=HTTP_406_NOT_ACCEPTABLE)
    return response


# Añadir cliente a categoria
@cliente.post("/cliente/categoria", response_model=cliente_categoria_schema.ClienteCategoriaOut)
def añadir_cliente_a_categoria(info_cliente_categoria: cliente_categoria_schema.ClienteCategoria,
                               db: Session = Depends(get_db)):
    response = crud.añadir_cliente_a_categoria(db=db, info_cliente_categoria=info_cliente_categoria)
    if response == "HTTP_406_NOT_ACCEPTABLE":
        response = Response(status_code=HTTP_406_NOT_ACCEPTABLE)
    return response


# Consultar saldo en cuentas
@cliente.get("/clientes/saldo", response_model=Dict[int, float])
def consultar_saldo(cliente_id: int, db: Session = Depends(get_db)):
    response = crud.consultar_saldo(db=db, cliente_id=cliente_id)
    if response == "HTTP_406_NOT_ACCEPTABLE":
        response = Response(status_code=HTTP_406_NOT_ACCEPTABLE)
    return response


# Consultar saldo en cuentas en dolares
@cliente.get("/clientes/saldo/dolar", response_model=Dict[int, float])
def consultar_saldo(cliente_id: int, db: Session = Depends(get_db)):
    response = crud.consultar_saldo(db=db, cliente_id=cliente_id, dolar=True)
    if response == "HTTP_406_NOT_ACCEPTABLE":
        response = Response(status_code=HTTP_406_NOT_ACCEPTABLE)
    return response
