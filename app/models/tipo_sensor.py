from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class TipoSensor(Base):

    __tablename__ = "tipos_sensor"

    id_tipo_sensor = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    nombre = Column(
        String(100),
        nullable=False
    )

    descripcion = Column(
        Text
    )

    fabricante = Column(
        String(100)
    )

    modelo = Column(
        String(100)
    )

    sensores = relationship(
        "Sensor",
        back_populates="tipo_sensor"
    )