from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.tipo_medicion import TipoMedicionService
from app.api.respuestas import convertir_a_dict, convertir_lista


router = APIRouter(
    prefix="/agua",
    tags=["Tipos de Medición"]
)


@router.get("/tipos-medicion")
def listar_tipos_medicion(
    db: Session = Depends(get_db)
):
    service = TipoMedicionService(db)

    datos = service.listar_tipos_medicion()

    return {
        "cantidad": len(datos),
        "datos": convertir_lista(datos)
    }


@router.get("/tipos-medicion/{id_tipo_medicion}")
def obtener_tipo_medicion(
    id_tipo_medicion: int,
    db: Session = Depends(get_db)
):
    service = TipoMedicionService(db)

    try:
        dato = service.obtener_tipo_medicion(id_tipo_medicion)

        return convertir_a_dict(dato)

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.post("/tipos-medicion")
def crear_tipo_medicion(
    datos: Dict[str, Any],
    db: Session = Depends(get_db)
):
    service = TipoMedicionService(db)

    try:
        dato = service.crear_tipo_medicion(datos)

        return {
            "mensaje": "Tipo de medición creado correctamente",
            "datos": convertir_a_dict(dato)
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.put("/tipos-medicion/{id_tipo_medicion}")
def actualizar_tipo_medicion(
    id_tipo_medicion: int,
    datos: Dict[str, Any],
    db: Session = Depends(get_db)
):
    service = TipoMedicionService(db)

    try:
        dato = service.actualizar_tipo_medicion(
            id_tipo_medicion,
            datos
        )

        return {
            "mensaje": "Tipo de medición actualizado correctamente",
            "datos": convertir_a_dict(dato)
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.delete("/tipos-medicion/{id_tipo_medicion}")
def eliminar_tipo_medicion(
    id_tipo_medicion: int,
    db: Session = Depends(get_db)
):
    service = TipoMedicionService(db)

    try:
        service.eliminar_tipo_medicion(id_tipo_medicion)

        return {
            "mensaje": "Tipo de medición eliminado correctamente"
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )