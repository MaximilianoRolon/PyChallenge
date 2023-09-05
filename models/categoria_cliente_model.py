from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from config.db import Base


class CategoriaCliente(Base):
    __tablename__ = "categoria_cliente"

    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey("cliente.id"))
    categoria_id = Column(Integer, ForeignKey("categoria.id"))


