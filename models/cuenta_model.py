from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from config.db import Base


class Cuenta(Base):
    __tablename__ = "cuenta"

    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey("cliente.id"))

    cliente = relationship("Cliente", back_populates="cuentas")
    movimientos = relationship("Movimiento", back_populates="cuenta")
