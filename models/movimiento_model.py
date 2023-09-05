from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from config.db import Base


class Movimiento(Base):
    __tablename__ = "movimiento"

    id = Column(Integer, primary_key=True)
    cuenta_id = Column(Integer, ForeignKey("cuenta.id"))
    tipo = Column(String(255))
    importe = Column(Integer)
    fecha = Column(String(255))

    cuenta = relationship("Cuenta", back_populates="movimientos")
