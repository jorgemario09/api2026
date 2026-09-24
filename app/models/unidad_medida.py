from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class UnidadMedida(Base):

    __tablename__ = "unidades_medida"

    id_unidad = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    nombre = Column(
        String(100),
        nullable=False
    )

    simbolo = Column(
        String(20),
        nullable=False
    )

    descripcion = Column(
        String(200)
    )

    tipos_medicion = relationship(
        "TipoMedicion",
        back_populates="unidad"
    )