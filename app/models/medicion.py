from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    String,
    DateTime,
    Numeric,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class Medicion(Base):

    __tablename__ = "mediciones"

    id_medicion = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    id_sensor = Column(
        Integer,
        ForeignKey("sensores.id_sensor"),
        nullable=False
    )

    valor = Column(
        Numeric(12, 4),
        nullable=False
    )

    fecha_hora = Column(
        DateTime,
        nullable=False
    )

    calidad_dato = Column(
        String(30),
        nullable=False,
        default="VALIDO"
    )

    sensor = relationship(
        "Sensor",
        back_populates="mediciones"
    )