from fastapi import APIRouter
from models.cliente import cliente as clientemodel
from config.db import conn

cliente = APIRouter()


@cliente.get("/clientes")
def devolverclientes():
    query = conn.execute(clientemodel.select()).fetchall()
    return [r._asdict() for r in query]
