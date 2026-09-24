from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.ubicacion import UbicacionService
from app.api.respuestas import convertir_a_dict, convertir_lista


router = APIRouter(
    prefix="/agua",
    tags=["Ubicaciones"]
)


@router.get("/ubicaciones")
def listar_ubicaciones(
    db: Session = Depends(get_db)
):
    service = UbicacionService(db)

    datos = service.listar_ubicaciones()

    return {
        "cantidad": len(datos),
        "datos": convertir_lista(datos)
    }


@router.get("/ubicaciones/{id_ubicacion}")
def obtener_ubicacion(
    id_ubicacion: int,
    db: Session = Depends(get_db)
):
    service = UbicacionService(db)

    try:
        dato = service.obtener_ubicacion(id_ubicacion)

        return convertir_a_dict(dato)

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.post("/ubicaciones")
def crear_ubicacion(
    datos: Dict[str, Any],
    db: Session = Depends(get_db)
):
    service = UbicacionService(db)

    try:
        dato = service.crear_ubicacion(datos)

        return {
            "mensaje": "Ubicación creada correctamente",
            "datos": convertir_a_dict(dato)
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.put("/ubicaciones/{id_ubicacion}")
def actualizar_ubicacion(
    id_ubicacion: int,
    datos: Dict[str, Any],
    db: Session = Depends(get_db)
):
    service = UbicacionService(db)

    try:
        dato = service.actualizar_ubicacion(
            id_ubicacion,
            datos
        )

        return {
            "mensaje": "Ubicación actualizada correctamente",
            "datos": convertir_a_dict(dato)
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.delete("/ubicaciones/{id_ubicacion}")
def eliminar_ubicacion(
    id_ubicacion: int,
    db: Session = Depends(get_db)
):
    service = UbicacionService(db)

    try:
        service.eliminar_ubicacion(id_ubicacion)

        return {
            "mensaje": "Ubicación eliminada correctamente"
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )