from fastapi import APIRouter, HTTPException
from app.services.influx_service import InfluxService

router = APIRouter(
    prefix="/agua",
    tags=["Telemetría InfluxDB"]
)

@router.get("/telemetria-mqtt")
def obtener_telemetria_mqtt(limite: int = 10):
    servicio = InfluxService()
    try:
        datos = servicio.obtener_ultimas_mediciones_mqtt(limite)
        return {
            "cantidad": len(datos),
            "datos": datos
        }
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )