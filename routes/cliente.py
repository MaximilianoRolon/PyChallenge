from fastapi import APIRouter
from starlette.responses import Response
from starlette.status import HTTP_204_NO_CONTENT

from models.cliente import cliente as clientemodel
from config.db import conn
from schemas.cliente import Cliente

cliente = APIRouter()


# TODO Añadir response_model y tags a todas las rutas


# Listar todos los clientes
@cliente.get("/clientes")
def devolver_clientes():
    result = conn.execute(clientemodel.select()).fetchall()
    return [r._asdict() for r in result]


# Añadir nuevo cliente
# TODO: validacion de cliente repetido
@cliente.post("/clientes")
def crear_cliente(cliente: Cliente):
    nuevo_cliente = {"nombre": cliente.nombre}
    conn.execute(clientemodel.insert().values(nuevo_cliente))
    return "nuevo_cliente"


# Consultar cliente con sus cuentas y categorias
@cliente.get("/clientes/{id}")
def devolver_info_cliente(id: str):
    result = conn.execute(clientemodel.select().where(clientemodel.c.id == id)).fetchall()
    return [r._asdict() for r in result]


# Eliminar cliente
# TODO: Responder si borro algo o no borro nada
@cliente.get("/clientes/eliminar/{id}")
def eliminar_cliente(id: str):
    result = conn.execute(clientemodel.delete().where(clientemodel.c.id == id))
    return Response(status_code=HTTP_204_NO_CONTENT)


# Actualizar nombre de cliente
# TODO: Responder si actualizo o no algo
@cliente.put("/clientes/{id}")
def actualizar_nombre_cliente(id: str, cliente: Cliente):
    result = conn.execute(clientemodel.update().values(nombre=cliente.nombre).where(clientemodel.c.id == id))
    return Response(status_code=HTTP_204_NO_CONTENT)
