from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.sensor import SensorService
from app.api.respuestas import convertir_a_dict, convertir_lista


router = APIRouter(
    prefix="/agua",
    tags=["Sensores"]
)


@router.get("/sensores")
def listar_sensores(
    db: Session = Depends(get_db)
):
    service = SensorService(db)

    datos = service.listar_sensores()

    return {
        "cantidad": len(datos),
        "datos": convertir_lista(datos)
    }


@router.get("/sensores/{id_sensor}")
def obtener_sensor(
    id_sensor: int,
    db: Session = Depends(get_db)
):
    service = SensorService(db)

    try:
        dato = service.obtener_sensor(id_sensor)

        return convertir_a_dict(dato)

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.post("/sensores")
def crear_sensor(
    datos: Dict[str, Any],
    db: Session = Depends(get_db)
):
    service = SensorService(db)

    try:
        dato = service.crear_sensor(datos)

        return {
            "mensaje": "Sensor creado correctamente",
            "datos": convertir_a_dict(dato)
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.put("/sensores/{id_sensor}")
def actualizar_sensor(
    id_sensor: int,
    datos: Dict[str, Any],
    db: Session = Depends(get_db)
):
    service = SensorService(db)

    try:
        dato = service.actualizar_sensor(
            id_sensor,
            datos
        )

        return {
            "mensaje": "Sensor actualizado correctamente",
            "datos": convertir_a_dict(dato)
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.delete("/sensores/{id_sensor}")
def eliminar_sensor(
    id_sensor: int,
    db: Session = Depends(get_db)
):
    service = SensorService(db)

    try:
        service.eliminar_sensor(id_sensor)

        return {
            "mensaje": "Sensor eliminado correctamente"
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )