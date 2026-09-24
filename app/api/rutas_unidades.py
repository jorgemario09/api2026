from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.unidad_medida import UnidadService
from app.api.respuestas import convertir_a_dict, convertir_lista


router = APIRouter(
    prefix="/agua",
    tags=["Unidades"]
)


@router.get("/unidades")
def listar_unidades(
    db: Session = Depends(get_db)
):
    service = UnidadService(db)

    datos = service.listar_unidades()

    return {
        "cantidad": len(datos),
        "datos": convertir_lista(datos)
    }


@router.get("/unidades/{id_unidad}")
def obtener_unidad(
    id_unidad: int,
    db: Session = Depends(get_db)
):
    service = UnidadService(db)

    try:
        dato = service.obtener_unidad(id_unidad)

        return convertir_a_dict(dato)

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.post("/unidades")
def crear_unidad(
    datos: Dict[str, Any],
    db: Session = Depends(get_db)
):
    service = UnidadService(db)

    try:
        dato = service.crear_unidad(datos)

        return {
            "mensaje": "Unidad creada correctamente",
            "datos": convertir_a_dict(dato)
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.put("/unidades/{id_unidad}")
def actualizar_unidad(
    id_unidad: int,
    datos: Dict[str, Any],
    db: Session = Depends(get_db)
):
    service = UnidadService(db)

    try:
        dato = service.actualizar_unidad(
            id_unidad,
            datos
        )

        return {
            "mensaje": "Unidad actualizada correctamente",
            "datos": convertir_a_dict(dato)
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.delete("/unidades/{id_unidad}")
def eliminar_unidad(
    id_unidad: int,
    db: Session = Depends(get_db)
):
    service = UnidadService(db)

    try:
        service.eliminar_unidad(id_unidad)

        return {
            "mensaje": "Unidad eliminada correctamente"
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )