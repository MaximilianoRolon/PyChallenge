from datetime import datetime

import requests
from sqlalchemy import update, delete
from sqlalchemy.orm import Session
from starlette.responses import Response
from starlette.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_406_NOT_ACCEPTABLE

from models import cuenta_model, cliente_model, movimiento_model, categoria_cliente_model, categoria_model
from schemas import cuenta_schema, cliente_schema, movimiento_schema, cliente_categoria_schema


# Registro de cliente en la DB tomando el schema de cliente
def registrar_cliente(db: Session, info_cliente: cliente_schema.Cliente):
    db_user = cliente_model.Cliente(nombre=info_cliente.nombre)
    db.add(db_user)
    db.commit()
    id_cliente = db_user.id
    db_user = cuenta_model.Cuenta(cliente_id=id_cliente)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

# Edicion de cliente en la DB tomando el schema de cliente
def editar_cliente(db: Session, info_cliente: cliente_schema.ClienteEdit):
    result = db.query(cliente_model.Cliente).filter(cliente_model.Cliente.id == info_cliente.id).first()
    if result:
        db.execute(update(cliente_model.Cliente).where(cliente_model.Cliente.id == info_cliente.id).values(
            nombre=info_cliente.nombre))
        db.commit()
    else:
        return Response(status_code=HTTP_406_NOT_ACCEPTABLE)


# Listado de todos los clientes
def listar_clientes(db: Session):
    return db.query(cliente_model.Cliente).all()


# Eliminacion de cliente en la DB tomando el schema de id de cliente
def eliminar_cliente(db: Session, info_clienteId: cliente_schema.ClienteId):
    cliente_result = db.query(cliente_model.Cliente).filter(cliente_model.Cliente.id == info_clienteId.id).first()
    if cliente_result:
        cuenta_result = db.query(cuenta_model.Cuenta).filter(cuenta_model.Cuenta.cliente_id == cliente_result.id).all()
        # Loop de cuentas del cliente
        if cuenta_result:
            for cuenta in cuenta_result:
                db.execute(
                    delete(movimiento_model.Movimiento).where(movimiento_model.Movimiento.cuenta_id == cuenta.id))
                db.commit()
                db.execute(delete(cuenta_model.Cuenta).where(cuenta_model.Cuenta.cliente_id == cliente_result.id))
                db.commit()
        db.execute(delete(categoria_cliente_model.CategoriaCliente).where(
            categoria_cliente_model.CategoriaCliente.cliente_id == info_clienteId.id))
        db.commit()
        db.execute(delete(cliente_model.Cliente).where(cliente_model.Cliente.id == info_clienteId.id))
        db.commit()
        result = cliente_result
    else:
        result = Response(status_code=HTTP_406_NOT_ACCEPTABLE)
    return result


# Registro de cliente en una categoria tomando el schema de cliente_categoria
def añadir_cliente_a_categoria(db: Session, info_cliente_categoria: cliente_categoria_schema.ClienteCategoria):
    cliente_result = db.query(cliente_model.Cliente).filter(
        cliente_model.Cliente.id == info_cliente_categoria.cliente_id).first()
    categoria_result = db.query(categoria_model.Categoria).filter(
        categoria_model.Categoria.id == info_cliente_categoria.categoria_id).first()
    if cliente_result and categoria_result:
        db_user = categoria_cliente_model.CategoriaCliente(cliente_id=info_cliente_categoria.cliente_id,
                                                           categoria_id=info_cliente_categoria.categoria_id)
        db.add(db_user)
        db.commit()
        result = db_user
    else:
        result = Response(status_code=HTTP_406_NOT_ACCEPTABLE)
    return result

# Consulta de cuentas y categorias tomando el id del cliente
def consultar_cuentas_y_categorias(db: Session, id: int):
    cliente_result = db.query(cliente_model.Cliente).filter(cliente_model.Cliente.id == id).first()
    if cliente_result:
        cuenta_result = db.query(cuenta_model.Cuenta).filter(cuenta_model.Cuenta.cliente_id == id).all()
        categoria_cliente_result = db.query(categoria_model.Categoria).join(categoria_cliente_model.CategoriaCliente, categoria_model.Categoria.id == categoria_cliente_model.CategoriaCliente.categoria_id).filter(categoria_cliente_model.CategoriaCliente.cliente_id == id).all()
        result =  cuenta_result, categoria_cliente_result
    else:
        result = Response(status_code=HTTP_406_NOT_ACCEPTABLE)
    return result


# Consulta de saldo tomando id del cliente
def consultar_saldo(db: Session, id: int, dolar=False):
    result = {}
    cliente_result = db.query(cliente_model.Cliente).filter(cliente_model.Cliente.id == id).first()
    if cliente_result:
        cuenta_result = db.query(cuenta_model.Cuenta).filter(cuenta_model.Cuenta.cliente_id == cliente_result.id).all()
        # Loop de cuentas del cliente
        if cuenta_result:
            for cuenta in cuenta_result:
                movimiento_result = db.query(cuenta_model.Movimiento).filter(
                    movimiento_model.Movimiento.cuenta_id == cuenta.id).all()
                if movimiento_result:
                    result[cuenta.id] = 0
                    for movimiento in movimiento_result:
                        if movimiento.tipo == "i":
                            result[cuenta.id] = result[cuenta.id] + movimiento.importe
                        else:
                            result[cuenta.id] = result[cuenta.id] - movimiento.importe

                    # Pasar a dolar si el parametro opcional esta en True
                    if dolar == True:
                        api_url = "https://www.dolarsi.com/api/api.php?type=valoresprincipales"
                        response = requests.get(api_url)
                        response.json()

                        valor_dolar_bolsa = None

                        for item in response.json():
                            if 'nombre' in item['casa'] and item['casa']['nombre'] == 'Dolar Bolsa':
                                valor_dolar_bolsa = item["casa"]["compra"]

                        result[cuenta.id] = round(result[cuenta.id] / float(valor_dolar_bolsa.replace(',', '.')), 2)
    else:
        result = Response(status_code=HTTP_406_NOT_ACCEPTABLE)
    return result


# Registro de movimiento tomando el schema de movimiento
def registrar_movimiento(db: Session, info_movimiento: movimiento_schema.Movimiento):
    result = None
    cuenta_result = db.query(cuenta_model.Cuenta).filter(cuenta_model.Cuenta.id == info_movimiento.cuenta_id).first()
    if cuenta_result:
        if info_movimiento.tipo == "e":
            movimiento_result = db.query(movimiento_model.Movimiento).filter(movimiento_model.Movimiento.cuenta_id == info_movimiento.cuenta_id).all()
            # Loop de movimientos de la cuenta
            saldo = 0
            if movimiento_result:
                for movimiento in movimiento_result:
                    if movimiento.tipo == "e":
                        saldo = saldo - movimiento.importe
                    if movimiento.tipo == "i":
                        saldo = saldo + movimiento.importe

            if saldo < info_movimiento.importe:
                result = Response(status_code=HTTP_406_NOT_ACCEPTABLE)

        if result == None:
            fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            db_user = movimiento_model.Movimiento(cuenta_id=info_movimiento.cuenta_id, tipo=info_movimiento.tipo, importe=info_movimiento.importe, fecha=fecha_actual)
            db.add(db_user)
            db.commit()
            result = db_user
        return result

#Eliminacion de movimiento tomando el schema de id de movimiento
def eliminar_movimiento(db: Session, info_movimientoId: movimiento_schema.MovimientoId):
    movimiento_result = db.query(movimiento_model.Movimiento).filter(movimiento_model.Movimiento.id == info_movimientoId.id).first()
    if movimiento_result:
        db.execute(delete(movimiento_model.Movimiento).where(movimiento_model.Movimiento.id == info_movimientoId.id))
        db.commit()
        return movimiento_result
    else:
        return Response(status_code=HTTP_406_NOT_ACCEPTABLE)



# Consulta de movimiento tomando el id de movimiento
def consultar_movimiento(db: Session, id: int):
    movimiento_result = db.query(movimiento_model.Movimiento).filter(movimiento_model.Movimiento.id == id).first()
    if movimiento_result:
        result = movimiento_result
    else:
        result = Response(status_code=HTTP_406_NOT_ACCEPTABLE)
    return result

