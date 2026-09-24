from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.umbral import UmbralService
from app.api.respuestas import convertir_a_dict, convertir_lista


router = APIRouter(
    prefix="/agua",
    tags=["Umbrales"]
)


@router.get("/umbrales")
def listar_umbrales(
    db: Session = Depends(get_db)
):
    service = UmbralService(db)

    datos = service.listar_umbrales()

    return {
        "cantidad": len(datos),
        "datos": convertir_lista(datos)
    }


@router.get("/umbrales/{id_umbral}")
def obtener_umbral(
    id_umbral: int,
    db: Session = Depends(get_db)
):
    service = UmbralService(db)

    try:
        dato = service.obtener_umbral(id_umbral)

        return convertir_a_dict(dato)

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.post("/umbrales")
def crear_umbral(
    datos: Dict[str, Any],
    db: Session = Depends(get_db)
):
    service = UmbralService(db)

    try:
        dato = service.crear_umbral(datos)

        return {
            "mensaje": "Umbral creado correctamente",
            "datos": convertir_a_dict(dato)
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.put("/umbrales/{id_umbral}")
def actualizar_umbral(
    id_umbral: int,
    datos: Dict[str, Any],
    db: Session = Depends(get_db)
):
    service = UmbralService(db)

    try:
        dato = service.actualizar_umbral(
            id_umbral,
            datos
        )

        return {
            "mensaje": "Umbral actualizado correctamente",
            "datos": convertir_a_dict(dato)
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.delete("/umbrales/{id_umbral}")
def eliminar_umbral(
    id_umbral: int,
    db: Session = Depends(get_db)
):
    service = UmbralService(db)

    try:
        service.eliminar_umbral(id_umbral)

        return {
            "mensaje": "Umbral eliminado correctamente"
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )
        