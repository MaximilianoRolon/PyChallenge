from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from models.categoria_cliente_model import CategoriaCliente
from models.categoria_model import Categoria
from config.db import Base


class Cliente(Base):
    __tablename__ = "cliente"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(255))

    cuentas = relationship("Cuenta", back_populates="cliente")
    categorias = relationship('Categoria', secondary='categoria_cliente', back_populates='clientes')
