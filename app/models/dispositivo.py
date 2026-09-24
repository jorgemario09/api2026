from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class Dispositivo(Base):

    __tablename__ = "dispositivos"

    id_dispositivo = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    nombre = Column(
        String(100),
        nullable=False
    )

    codigo = Column(
        String(50),
        unique=True,
        nullable=False
    )

    id_ubicacion = Column(
        Integer,
        ForeignKey("ubicaciones.id_ubicacion"),
        nullable=False
    )

    fecha_registro = Column(
        DateTime,
        nullable=False
    )

    estado = Column(
        Boolean,
        nullable=False,
        default=True
    )

    ubicacion = relationship(
        "Ubicacion",
        back_populates="dispositivos"
    )

    sensores = relationship(
        "Sensor",
        back_populates="dispositivo"
    )

    eventos = relationship(
        "Evento",
        back_populates="dispositivo"
    )

    estados = relationship(
        "EstadoDispositivo",
        back_populates="dispositivo"
    )