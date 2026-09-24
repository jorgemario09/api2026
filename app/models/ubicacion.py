from sqlalchemy import Column, Integer, String, Numeric, Boolean
from sqlalchemy.orm import relationship

from app.core.database import Base


class Ubicacion(Base):

    __tablename__ = "ubicaciones"

    id_ubicacion = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    nombre = Column(
        String(100),
        nullable=False
    )

    descripcion = Column(
        String(200)
    )

    latitud = Column(
        Numeric(10, 7)
    )

    longitud = Column(
        Numeric(10, 7)
    )

    estado = Column(
        Boolean,
        nullable=False,
        default=True
    )

    dispositivos = relationship(
        "Dispositivo",
        back_populates="ubicacion"
    )