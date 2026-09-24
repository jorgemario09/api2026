from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.tipo_evento import TipoEventoService
from app.api.respuestas import convertir_a_dict, convertir_lista


router = APIRouter(
    prefix="/agua",
    tags=["Tipos de Evento"]
)


@router.get("/tipos-evento")
def listar_tipos_evento(
    db: Session = Depends(get_db)
):
    service = TipoEventoService(db)

    datos = service.listar_tipos_evento()

    return {
        "cantidad": len(datos),
        "datos": convertir_lista(datos)
    }


@router.get("/tipos-evento/{id_tipo_evento}")
def obtener_tipo_evento(
    id_tipo_evento: int,
    db: Session = Depends(get_db)
):
    service = TipoEventoService(db)

    try:
        dato = service.obtener_tipo_evento(id_tipo_evento)

        return convertir_a_dict(dato)

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.post("/tipos-evento")
def crear_tipo_evento(
    datos: Dict[str, Any],
    db: Session = Depends(get_db)
):
    service = TipoEventoService(db)

    try:
        dato = service.crear_tipo_evento(datos)

        return {
            "mensaje": "Tipo de evento creado correctamente",
            "datos": convertir_a_dict(dato)
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.put("/tipos-evento/{id_tipo_evento}")
def actualizar_tipo_evento(
    id_tipo_evento: int,
    datos: Dict[str, Any],
    db: Session = Depends(get_db)
):
    service = TipoEventoService(db)

    try:
        dato = service.actualizar_tipo_evento(
            id_tipo_evento,
            datos
        )

        return {
            "mensaje": "Tipo de evento actualizado correctamente",
            "datos": convertir_a_dict(dato)
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.delete("/tipos-evento/{id_tipo_evento}")
def eliminar_tipo_evento(
    id_tipo_evento: int,
    db: Session = Depends(get_db)
):
    service = TipoEventoService(db)

    try:
        service.eliminar_tipo_evento(id_tipo_evento)

        return {
            "mensaje": "Tipo de evento eliminado correctamente"
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )