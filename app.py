from fastapi import FastAPI
from routes.cliente import cliente

app = FastAPI()

app.include_router(cliente)
