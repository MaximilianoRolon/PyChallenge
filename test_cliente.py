import pytest
from fastapi.testclient import TestClient
from pydantic import json

from app import app

client = TestClient(app)


def test_consultar_cuentas_y_categorias():

    response = client.get("/clientes/1")
    assert response.status_code == 200 or response.status_code == 406

    response = client.get("/clientes/2")
    assert response.status_code == 200 or response.status_code == 406

    response = client.get("/clientes/24212")
    assert response.status_code == 200 or response.status_code == 406

    response = client.get("/clientes/asdasd")
    assert response.status_code == 422


def test_listar_clientes():
    response = client.get("/clientes")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"


def test_consultar_saldo():
    response = client.get("/clientes/saldo/1")
    assert response.status_code == 200 or response.status_code == 406

    response = client.get("/clientes/saldo/2")
    assert response.status_code == 200 or response.status_code == 406

    response = client.get("/clientes/saldo/24212")
    assert response.status_code == 200 or response.status_code == 406

    response = client.get("/clientes/saldo/asdasd")
    assert response.status_code == 422


def test_consultar_saldo_dolar():
    response = client.get("/clientes/saldo/dolar/1")
    assert response.status_code == 200 or response.status_code == 406

    response = client.get("/clientes/saldo/dolar/2")
    assert response.status_code == 200 or response.status_code == 406

    response = client.get("/clientes/saldo/dolar/24212")
    assert response.status_code == 200 or response.status_code == 406

    response = client.get("/clientes/saldo/dolar/asdasd")
    assert response.status_code == 422


def test_consultar_movimiento():

    response = client.get("/movimientos/1")
    assert response.status_code == 200 or response.status_code == 406

    response = client.get("/movimientos/2")
    assert response.status_code == 200 or response.status_code == 406

    response = client.get("/movimientos/24212")
    assert response.status_code == 200 or response.status_code == 406

    response = client.get("/movimientos/asdasd")
    assert response.status_code == 422
