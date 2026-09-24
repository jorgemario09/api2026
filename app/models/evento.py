from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    Text,
    String,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class Evento(Base):

    __tablename__ = "eventos"

    id_evento = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    id_tipo_evento = Column(
        Integer,
        ForeignKey("tipos_evento.id_tipo_evento"),
        nullable=False
    )

    id_dispositivo = Column(
        Integer,
        ForeignKey("dispositivos.id_dispositivo"),
        nullable=False
    )

    fecha_hora = Column(
        DateTime,
        nullable=False
    )

    descripcion = Column(
        Text
    )

    estado = Column(
        String(30),
        nullable=False
    )

    tipo_evento = relationship(
        "TipoEvento",
        back_populates="eventos"
    )

    dispositivo = relationship(
        "Dispositivo",
        back_populates="eventos"
    )