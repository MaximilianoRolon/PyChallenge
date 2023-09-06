from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship
from config.db import Base
from sqlalchemy import DECIMAL
from data_type.enums import TipoEnum


class Movimiento(Base):
    __tablename__ = "movimiento"

    id = Column(Integer, primary_key=True)
    cuenta_id = Column(Integer, ForeignKey("cuenta.id"))
    tipo = Column(String(1))
    importe = Column(DECIMAL(10, 2))
    fecha = Column(String(255))

    cuenta = relationship("Cuenta", back_populates="movimientos")
