from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class TipoEvento(Base):

    __tablename__ = "tipos_evento"

    id_tipo_evento = Column(
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

    nivel = Column(
        String(30),
        nullable=False
    )

    eventos = relationship(
        "Evento",
        back_populates="tipo_evento"
    )