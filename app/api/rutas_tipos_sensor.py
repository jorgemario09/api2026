from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.tipo_sensor import TipoSensorService
from app.api.respuestas import convertir_a_dict, convertir_lista


router = APIRouter(
    prefix="/agua",
    tags=["Tipos de Sensor"]
)


@router.get("/tipos-sensor")
def listar_tipos_sensor(
    db: Session = Depends(get_db)
):
    service = TipoSensorService(db)

    datos = service.listar_tipos_sensor()

    return {
        "cantidad": len(datos),
        "datos": convertir_lista(datos)
    }


@router.get("/tipos-sensor/{id_tipo_sensor}")
def obtener_tipo_sensor(
    id_tipo_sensor: int,
    db: Session = Depends(get_db)
):
    service = TipoSensorService(db)

    try:
        dato = service.obtener_tipo_sensor(id_tipo_sensor)

        return convertir_a_dict(dato)

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.post("/tipos-sensor")
def crear_tipo_sensor(
    datos: Dict[str, Any],
    db: Session = Depends(get_db)
):
    service = TipoSensorService(db)

    try:
        dato = service.crear_tipo_sensor(datos)

        return {
            "mensaje": "Tipo de sensor creado correctamente",
            "datos": convertir_a_dict(dato)
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.put("/tipos-sensor/{id_tipo_sensor}")
def actualizar_tipo_sensor(
    id_tipo_sensor: int,
    datos: Dict[str, Any],
    db: Session = Depends(get_db)
):
    service = TipoSensorService(db)

    try:
        dato = service.actualizar_tipo_sensor(
            id_tipo_sensor,
            datos
        )

        return {
            "mensaje": "Tipo de sensor actualizado correctamente",
            "datos": convertir_a_dict(dato)
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.delete("/tipos-sensor/{id_tipo_sensor}")
def eliminar_tipo_sensor(
    id_tipo_sensor: int,
    db: Session = Depends(get_db)
):
    service = TipoSensorService(db)

    try:
        service.eliminar_tipo_sensor(id_tipo_sensor)

        return {
            "mensaje": "Tipo de sensor eliminado correctamente"
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )