from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.dispositivo import DispositivoService
from app.api.respuestas import convertir_a_dict, convertir_lista


router = APIRouter(
    prefix="/agua",
    tags=["Dispositivos"]
)


@router.get("/dispositivos")
def listar_dispositivos(
    db: Session = Depends(get_db)
):
    service = DispositivoService(db)

    datos = service.listar_dispositivos()

    return {
        "cantidad": len(datos),
        "datos": convertir_lista(datos)
    }


@router.get("/dispositivos/{id_dispositivo}")
def obtener_dispositivo(
    id_dispositivo: int,
    db: Session = Depends(get_db)
):
    service = DispositivoService(db)

    try:
        dato = service.obtener_dispositivo(id_dispositivo)

        return convertir_a_dict(dato)

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.post("/dispositivos")
def crear_dispositivo(
    datos: Dict[str, Any],
    db: Session = Depends(get_db)
):
    service = DispositivoService(db)

    try:
        dato = service.crear_dispositivo(datos)

        return {
            "mensaje": "Dispositivo creado correctamente",
            "datos": convertir_a_dict(dato)
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.put("/dispositivos/{id_dispositivo}")
def actualizar_dispositivo(
    id_dispositivo: int,
    datos: Dict[str, Any],
    db: Session = Depends(get_db)
):
    service = DispositivoService(db)

    try:
        dato = service.actualizar_dispositivo(
            id_dispositivo,
            datos
        )

        return {
            "mensaje": "Dispositivo actualizado correctamente",
            "datos": convertir_a_dict(dato)
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.delete("/dispositivos/{id_dispositivo}")
def eliminar_dispositivo(
    id_dispositivo: int,
    db: Session = Depends(get_db)
):
    service = DispositivoService(db)

    try:
        service.eliminar_dispositivo(id_dispositivo)

        return {
            "mensaje": "Dispositivo eliminado correctamente"
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )