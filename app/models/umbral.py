from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Numeric,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class Umbral(Base):

    __tablename__ = "umbrales"

    id_umbral = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    id_tipo_medicion = Column(
        Integer,
        ForeignKey("tipos_medicion.id_tipo_medicion"),
        nullable=False
    )

    valor_minimo = Column(
        Numeric(12, 4)
    )

    valor_maximo = Column(
        Numeric(12, 4)
    )

    nivel_alerta = Column(
        String(30),
        nullable=False
    )

    estado = Column(
        Boolean,
        nullable=False,
        default=True
    )

    tipo_medicion = relationship(
        "TipoMedicion",
        back_populates="umbrales"
    )