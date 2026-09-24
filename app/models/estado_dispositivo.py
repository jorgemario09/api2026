from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class EstadoDispositivo(Base):

    __tablename__ = "estados_dispositivo"

    id_estado = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    id_dispositivo = Column(
        Integer,
        ForeignKey("dispositivos.id_dispositivo"),
        nullable=False
    )

    estado = Column(
        String(30),
        nullable=False
    )

    fecha_hora = Column(
        DateTime,
        nullable=False
    )

    descripcion = Column(
        Text
    )

    dispositivo = relationship(
        "Dispositivo",
        back_populates="estados"
    )