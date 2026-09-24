from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.evento import EventoService
from app.api.respuestas import convertir_a_dict, convertir_lista


router = APIRouter(
    prefix="/agua",
    tags=["Eventos"]
)


@router.get("/eventos")
def listar_eventos(
    db: Session = Depends(get_db)
):
    service = EventoService(db)

    datos = service.listar_eventos()

    return {
        "cantidad": len(datos),
        "datos": convertir_lista(datos)
    }


@router.get("/eventos/{id_evento}")
def obtener_evento(
    id_evento: int,
    db: Session = Depends(get_db)
):
    service = EventoService(db)

    try:
        dato = service.obtener_evento(id_evento)

        return convertir_a_dict(dato)

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.post("/eventos")
def crear_evento(
    datos: Dict[str, Any],
    db: Session = Depends(get_db)
):
    service = EventoService(db)

    try:
        dato = service.crear_evento(datos)

        return {
            "mensaje": "Evento creado correctamente",
            "datos": convertir_a_dict(dato)
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.put("/eventos/{id_evento}")
def actualizar_evento(
    id_evento: int,
    datos: Dict[str, Any],
    db: Session = Depends(get_db)
):
    service = EventoService(db)

    try:
        dato = service.actualizar_evento(
            id_evento,
            datos
        )

        return {
            "mensaje": "Evento actualizado correctamente",
            "datos": convertir_a_dict(dato)
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.delete("/eventos/{id_evento}")
def eliminar_evento(
    id_evento: int,
    db: Session = Depends(get_db)
):
    service = EventoService(db)

    try:
        service.eliminar_evento(id_evento)

        return {
            "mensaje": "Evento eliminado correctamente"
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )