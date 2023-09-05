from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_consultar_cuentas_y_categorias():

    response = client.get("/clientes/info?cliente_id=1")
    assert response.status_code == 200 or response.status_code == 406

    response = client.get("/clientes/info?cliente_id=2")
    assert response.status_code == 200 or response.status_code == 406

    response = client.get("/clientes/info?cliente_id=24212")
    assert response.status_code == 200 or response.status_code == 406

    response = client.get("/clientes/info?cliente_id=asdasd")
    assert response.status_code == 422


def test_listar_clientes():
    response = client.get("/clientes")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"


def test_consultar_saldo():
    response = client.get("/clientes/saldo?cliente_id=1")
    assert response.status_code == 200 or response.status_code == 406

    response = client.get("/clientes/saldo?cliente_id=2")
    assert response.status_code == 200 or response.status_code == 406

    response = client.get("/clientes/saldo?cliente_id=24212")
    assert response.status_code == 200 or response.status_code == 406

    response = client.get("/clientes/saldo?cliente_id=asdasd")
    assert response.status_code == 422


def test_consultar_saldo_dolar():
    response = client.get("/clientes/saldo/dolar?cliente_id=1")
    assert response.status_code == 200 or response.status_code == 406

    response = client.get("/clientes/saldo/dolar?cliente_id=2")
    assert response.status_code == 200 or response.status_code == 406

    response = client.get("/clientes/saldo/dolar?cliente_id=24212")
    assert response.status_code == 200 or response.status_code == 406

    response = client.get("/clientes/saldo/dolar?cliente_id=asdasd")
    assert response.status_code == 422


def test_consultar_movimiento():

    response = client.get("/movimientos?movimiento_id=1")
    assert response.status_code == 200 or response.status_code == 406

    response = client.get("/movimientos?movimiento_id=2")
    assert response.status_code == 200 or response.status_code == 406

    response = client.get("/movimientos?movimiento_id=24212")
    assert response.status_code == 200 or response.status_code == 406

    response = client.get("/movimientos?movimiento_id=asdasd")
    assert response.status_code == 422
