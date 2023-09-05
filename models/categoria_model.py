from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.db import Base


class Categoria(Base):
    __tablename__ = "categoria"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(255))

    clientes = relationship('Cliente', secondary='categoria_cliente', back_populates='categorias')
