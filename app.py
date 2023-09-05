from fastapi import FastAPI
from routes.cliente import cliente
from routes.movimiento import movimiento
from config.db import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(cliente)
app.include_router(movimiento)
