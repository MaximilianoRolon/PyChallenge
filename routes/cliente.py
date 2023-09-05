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


# TODO Añadir response_model y tags a todas las rutas


# Consultar cuentas y categorias de un cliente
@cliente.get("/clientes/{id}")
def consultar_cuentas_y_categorias(id: int, db: Session = Depends(get_db)):
    return crud.consultar_cuentas_y_categorias(db=db, id=id)


# Registrar un cliente
@cliente.post("/clientes/")
def registrar_cliente(cliente: cliente_schema.Cliente, db: Session = Depends(get_db)):
    return crud.registrar_cliente(db=db, nombre_cliente=cliente)


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
@cliente.post("/cliente/eliminar/{id}")
def eliminar_cliente(id: int, db: Session = Depends(get_db)):
    return crud.eliminar_cliente(db=db, id=id)


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



'''

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


'''
