from sqlalchemy import Column, String, Numeric, DateTime
from app.core.database import Base


class VwMedicionOptimizada(Base):
    __tablename__ = "vw_mediciones_optimizada"

    # Se marcan nombre_sensor y fecha_hora como primary_key=True
    # para que SQLAlchemy pueda identificar los registros de la vista.
    nombre_sensor = Column(String(100), primary_key=True)
    medicion = Column(Numeric(12, 4))
    tipo_medicion = Column(String(100))
    fecha_hora = Column(DateTime, primary_key=True)