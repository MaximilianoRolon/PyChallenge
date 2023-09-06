from datetime import datetime

import requests
from typing import Dict, List, Tuple
from sqlalchemy import update, delete, Float
from sqlalchemy.orm import Session
from data_type.enums import TipoEnum

from models import cuenta_model, cliente_model, movimiento_model, categoria_cliente_model, categoria_model
from schemas import cliente_schema, movimiento_schema, cliente_categoria_schema, cuenta_schema, categoria_schema


# Registro de cliente en la DB tomando el schema de cliente
def registrar_cliente(db: Session, info_cliente: cliente_schema.Cliente) -> cuenta_schema.CuentaOut:
    db_user = cliente_model.Cliente(nombre=info_cliente.nombre)
    db.add(db_user)
    db.flush()
    id_cliente = db_user.id
    db_user = cuenta_model.Cuenta(cliente_id=id_cliente)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


# Edicion de cliente en la DB tomando el schema de cliente
def editar_cliente(db: Session, info_cliente: cliente_schema.ClienteEdit) -> cliente_schema.ClienteOut:
    result = db.query(cliente_model.Cliente).filter(cliente_model.Cliente.id == info_cliente.id).first()
    if result is None:
        result = "HTTP_406_NOT_ACCEPTABLE"
    else:
        db.execute(update(cliente_model.Cliente).where(cliente_model.Cliente.id == info_cliente.id).values(
            nombre=info_cliente.nombre))
        db.commit()
    return result


# Listado de todos los clientes
def listar_clientes(db: Session) -> List[cliente_schema.Cliente]:
    return db.query(cliente_model.Cliente).all()


# Eliminacion de cliente en la DB tomando el schema de id de cliente
def eliminar_cliente(db: Session, info_cliente_id: cliente_schema.ClienteId) -> int:
    cliente_result = db.query(cliente_model.Cliente).filter(cliente_model.Cliente.id == info_cliente_id.id).first()
    result = info_cliente_id.id
    if cliente_result is None:
        result = "HTTP_406_NOT_ACCEPTABLE"
    else:
        cuenta_result = db.query(cuenta_model.Cuenta).filter(cuenta_model.Cuenta.cliente_id == cliente_result.id).all()
        # Loop de cuentas del cliente
        if cuenta_result:
            for cuenta in cuenta_result:
                db.execute(
                    delete(movimiento_model.Movimiento).where(movimiento_model.Movimiento.cuenta_id == cuenta.id))
                db.execute(delete(cuenta_model.Cuenta).where(cuenta_model.Cuenta.cliente_id == cliente_result.id))
        db.execute(delete(categoria_cliente_model.CategoriaCliente).where(
            categoria_cliente_model.CategoriaCliente.cliente_id == info_cliente_id.id))
        db.execute(delete(cliente_model.Cliente).where(cliente_model.Cliente.id == info_cliente_id.id))
        db.commit()

    return result


# Registro de cliente en una categoria tomando el schema de cliente_categoria
def añadir_cliente_a_categoria(db: Session,
                               info_cliente_categoria: cliente_categoria_schema.ClienteCategoria) \
        -> cliente_categoria_schema.ClienteCategoriaOut:
    cliente_result = db.query(cliente_model.Cliente).filter(
        cliente_model.Cliente.id == info_cliente_categoria.cliente_id).first()
    categoria_result = db.query(categoria_model.Categoria).filter(
        categoria_model.Categoria.id == info_cliente_categoria.categoria_id).first()
    if cliente_result is None and categoria_result is None:
        result = "HTTP_406_NOT_ACCEPTABLE"
    else:
        db_user = categoria_cliente_model.CategoriaCliente(cliente_id=info_cliente_categoria.cliente_id,
                                                           categoria_id=info_cliente_categoria.categoria_id)
        db.add(db_user)
        db.commit()
        result = db_user
    return result


# Consulta de cuentas y categorias tomando el id del cliente
def consultar_cuentas_y_categorias(db: Session, cliente_id: int) -> Tuple[
 List[cuenta_schema.CuentaOut], List[categoria_schema.CategoriaOut]]:
    cliente_result = db.query(cliente_model.Cliente).filter(cliente_model.Cliente.id == cliente_id).first()
    if cliente_result is None:
        result = "HTTP_406_NOT_ACCEPTABLE"
    else:
        cuenta_result = db.query(cuenta_model.Cuenta).filter(cuenta_model.Cuenta.cliente_id == cliente_id).all()
        categoria_cliente_result = db.query(
            categoria_model.Categoria).join(categoria_cliente_model.CategoriaCliente,
                                            categoria_model.Categoria.id ==
                                            categoria_cliente_model.CategoriaCliente.categoria_id).filter(
            categoria_cliente_model.CategoriaCliente.cliente_id == cliente_id).all()
        result = cuenta_result, categoria_cliente_result
    return result


# Consulta de saldo tomando id del cliente
def consultar_saldo(db: Session, cliente_id: int, dolar=False) -> Dict[int, float]:
    result = {}
    cliente_result = db.query(cliente_model.Cliente).filter(cliente_model.Cliente.id == cliente_id).first()
    if cliente_result is None:
        result = "HTTP_406_NOT_ACCEPTABLE"
    else:
        cuenta_result = db.query(cuenta_model.Cuenta).filter(cuenta_model.Cuenta.cliente_id == cliente_result.id).all()
        # Loop de cuentas del cliente
        if cuenta_result:
            for cuenta in cuenta_result:
                movimiento_result = db.query(movimiento_model.Movimiento).filter(
                    movimiento_model.Movimiento.cuenta_id == cuenta.id).all()
                if movimiento_result:
                    result[cuenta.id] = 0
                    for movimiento in movimiento_result:
                        if movimiento.tipo == TipoEnum.INGRESO:
                            result[cuenta.id] = result[cuenta.id] + movimiento.importe
                        else:
                            result[cuenta.id] = result[cuenta.id] - movimiento.importe

                    # Pasar a dolar si el parametro opcional esta en True
                    if dolar:
                        api_url = "https://www.dolarsi.com/api/api.php?type=valoresprincipales"
                        response = requests.get(api_url)
                        response.json()

                        valor_dolar_bolsa = None

                        for item in response.json():
                            if 'nombre' in item['casa'] and item['casa']['nombre'] == 'Dolar Bolsa':
                                valor_dolar_bolsa = item["casa"]["compra"]

                        result[cuenta.id] = round(result[cuenta.id] / float(valor_dolar_bolsa.replace(',', '.')), 2)
    return result


# Registro de movimiento tomando el schema de movimiento
def registrar_movimiento(db: Session, info_movimiento: movimiento_schema.Movimiento) -> movimiento_schema.MovimientoOut:
    result = None
    cuenta_result = db.query(cuenta_model.Cuenta).filter(cuenta_model.Cuenta.id == info_movimiento.cuenta_id).first()
    if cuenta_result:
        if info_movimiento.tipo == TipoEnum.EGRESO:
            saldo = devolver_saldo(db, info_movimiento)

            if saldo < info_movimiento.importe:
                result = "HTTP_406_NOT_ACCEPTABLE"

        if result is None:
            fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            db_user = movimiento_model.Movimiento(cuenta_id=info_movimiento.cuenta_id, tipo=info_movimiento.tipo,
                                                  importe=info_movimiento.importe, fecha=fecha_actual)
            db.add(db_user)
            db.commit()
            result = db_user
        return result


# Eliminacion de movimiento tomando el schema de id de movimiento
def eliminar_movimiento(db: Session, info_movimiento_id: movimiento_schema.MovimientoId) -> int:
    movimiento_result = db.query(movimiento_model.Movimiento).filter(
        movimiento_model.Movimiento.id == info_movimiento_id.id).first()
    result = info_movimiento_id.id
    if movimiento_result is None:
        result = "HTTP_406_NOT_ACCEPTABLE"
    else:
        db.execute(delete(movimiento_model.Movimiento).where(movimiento_model.Movimiento.id == info_movimiento_id.id))
        db.commit()

    return result


# Consulta de movimiento tomando el id de movimiento
def consultar_movimiento(db: Session, movimiento_id: int) -> movimiento_schema.MovimientoOut:
    movimiento_result = db.query(movimiento_model.Movimiento).filter(
        movimiento_model.Movimiento.id == movimiento_id).first()
    if movimiento_result is None:
        result = "HTTP_406_NOT_ACCEPTABLE"
    else:
        result = movimiento_result
    return result


def devolver_saldo(db: Session, info_movimiento: movimiento_schema.Movimiento) -> Float:
    movimiento_result = db.query(movimiento_model.Movimiento).filter(
        movimiento_model.Movimiento.cuenta_id == info_movimiento.cuenta_id).all()
    # Loop de movimientos de la cuenta
    saldo = 0
    if movimiento_result:
        for movimiento in movimiento_result:
            if movimiento.tipo == TipoEnum.EGRESO:
                saldo = saldo - movimiento.importe
            if movimiento.tipo == TipoEnum.INGRESO:
                saldo = saldo + movimiento.importe

    result = saldo

    return result
