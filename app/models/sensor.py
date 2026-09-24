from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Date,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class Sensor(Base):

    __tablename__ = "sensores"

    id_sensor = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    codigo_sensor = Column(
        String(50),
        unique=True,
        nullable=False
    )

    id_tipo_sensor = Column(
        Integer,
        ForeignKey("tipos_sensor.id_tipo_sensor"),
        nullable=False
    )

    id_tipo_medicion = Column(
        Integer,
        ForeignKey("tipos_medicion.id_tipo_medicion"),
        nullable=False
    )

    id_dispositivo = Column(
        Integer,
        ForeignKey("dispositivos.id_dispositivo"),
        nullable=False
    )

    fecha_instalacion = Column(
        Date,
        nullable=False
    )

    estado = Column(
        Boolean,
        nullable=False,
        default=True
    )

    tipo_sensor = relationship(
        "TipoSensor",
        back_populates="sensores"
    )

    tipo_medicion = relationship(
        "TipoMedicion",
        back_populates="sensores"
    )

    dispositivo = relationship(
        "Dispositivo",
        back_populates="sensores"
    )

    mediciones = relationship(
        "Medicion",
        back_populates="sensor"
    )