from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.medicion import MedicionService
from app.api.respuestas import convertir_a_dict, convertir_lista


router = APIRouter(
    prefix="/agua",
    tags=["Mediciones"]
)


# =========================================================
# MEDICIONES
# =========================================================


@router.get("/mediciones")
def listar_mediciones(
    limit: Optional[int] = None,   # Parámetro estándar en inglés
    limite: Optional[int] = None,  # Parámetro alias para la app móvil/web
    db: Session = Depends(get_db)
):
    # Soporta tanto ?limit=20 como ?limite=20
    max_registros = limit if limit is not None else limite

    service = MedicionService(db)
    # Delega la paginación a la base de datos de Neon a través del servicio
    datos = service.listar_mediciones(limit=max_registros)

    return {
        "cantidad": len(datos),
        "datos": convertir_lista(datos)
    }


@router.get("/mediciones/{id_medicion}")
def obtener_medicion(
    id_medicion: int,
    db: Session = Depends(get_db)
):
    service = MedicionService(db)

    try:
        dato = service.obtener_medicion(
            id_medicion
        )

        return convertir_a_dict(dato)

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.post("/mediciones")
def crear_medicion(
    datos: Dict[str, Any],
    db: Session = Depends(get_db)
):
    service = MedicionService(db)

    try:
        dato = service.crear_medicion(
            datos
        )

        return {
            "mensaje": "Medición creada correctamente",
            "datos": convertir_a_dict(dato)
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.put("/mediciones/{id_medicion}")
def actualizar_medicion(
    id_medicion: int,
    datos: Dict[str, Any],
    db: Session = Depends(get_db)
):
    service = MedicionService(db)

    try:
        dato = service.actualizar_medicion(
            id_medicion,
            datos
        )

        return {
            "mensaje": "Medición actualizada correctamente",
            "datos": convertir_a_dict(dato)
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.delete("/mediciones/{id_medicion}")
def eliminar_medicion(
    id_medicion: int,
    db: Session = Depends(get_db)
):
    service = MedicionService(db)

    try:
        service.eliminar_medicion(
            id_medicion
        )

        return {
            "mensaje": "Medición eliminada correctamente"
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )
