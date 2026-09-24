from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.estado_dispositivo import EstadoService
from app.api.respuestas import convertir_a_dict, convertir_lista


router = APIRouter(
    prefix="/agua",
    tags=["Estados"]
)


@router.get("/estados")
def listar_estados(
    db: Session = Depends(get_db)
):
    service = EstadoService(db)

    datos = service.listar_estados()

    return {
        "cantidad": len(datos),
        "datos": convertir_lista(datos)
    }


@router.get("/estados/{id_estado}")
def obtener_estado(
    id_estado: int,
    db: Session = Depends(get_db)
):
    service = EstadoService(db)

    try:
        dato = service.obtener_estado(id_estado)

        return convertir_a_dict(dato)

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.post("/estados")
def crear_estado(
    datos: Dict[str, Any],
    db: Session = Depends(get_db)
):
    service = EstadoService(db)

    try:
        dato = service.crear_estado(datos)

        return {
            "mensaje": "Estado creado correctamente",
            "datos": convertir_a_dict(dato)
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.put("/estados/{id_estado}")
def actualizar_estado(
    id_estado: int,
    datos: Dict[str, Any],
    db: Session = Depends(get_db)
):
    service = EstadoService(db)

    try:
        dato = service.actualizar_estado(
            id_estado,
            datos
        )

        return {
            "mensaje": "Estado actualizado correctamente",
            "datos": convertir_a_dict(dato)
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.delete("/estados/{id_estado}")
def eliminar_estado(
    id_estado: int,
    db: Session = Depends(get_db)
):
    service = EstadoService(db)

    try:
        service.eliminar_estado(id_estado)

        return {
            "mensaje": "Estado eliminado correctamente"
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )