from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class TipoMedicion(Base):

    __tablename__ = "tipos_medicion"

    id_tipo_medicion = Column(
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

    id_unidad = Column(
        Integer,
        ForeignKey("unidades_medida.id_unidad"),
        nullable=False
    )

    unidad = relationship(
        "UnidadMedida",
        back_populates="tipos_medicion"
    )

    sensores = relationship(
        "Sensor",
        back_populates="tipo_medicion"
    )

    umbrales = relationship(
        "Umbral",
        back_populates="tipo_medicion"
    )