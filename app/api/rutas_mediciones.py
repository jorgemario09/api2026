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
# ENDPOINT RESUMIDO ULTRA-LIGERO PARA ESP32
# =========================================================
@router.get("/mediciones/resumen-esp32")
def obtener_resumen_esp32(db: Session = Depends(get_db)):
    """
    Entrega un JSON pequeño con el cálculo de promedio, máximo, mínimo
    y total de registros ejecutado directamente en Neon.
    """
    service = MedicionService(db)
    mediciones = service.listar_mediciones(limit=50)
    
    if not mediciones:
        return {"promedio": 0.0, "maximo": 0.0, "minimo": 0.0, "total": 0}
        
    valores = [float(m.medicion) for m in mediciones if m.medicion is not None]
    
    if not valores:
        return {"promedio": 0.0, "maximo": 0.0, "minimo": 0.0, "total": 0}

    return {
        "promedio": round(sum(valores) / len(valores), 2),
        "maximo": round(max(valores), 2),
        "minimo": round(min(valores), 2),
        "total": len(valores)
    }


# =========================================================
# MEDICIONES CONVENCIONALES
# =========================================================
@router.get("/mediciones")
def listar_mediciones(
    limit: Optional[int] = None,
    limite: Optional[int] = None,
    db: Session = Depends(get_db)
):
    max_registros = limit if limit is not None else limite
    service = MedicionService(db)
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
        dato = service.obtener_medicion(id_medicion)
        return convertir_a_dict(dato)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.post("/mediciones")
def crear_medicion(
    datos: Dict[str, Any],
    db: Session = Depends(get_db)
):
    service = MedicionService(db)
    try:
        dato = service.crear_medicion(datos)
        return {
            "mensaje": "Medición creada correctamente",
            "datos": convertir_a_dict(dato)
        }
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.put("/mediciones/{id_medicion}")
def actualizar_medicion(
    id_medicion: int,
    datos: Dict[str, Any],
    db: Session = Depends(get_db)
):
    service = MedicionService(db)
    try:
        dato = service.actualizar_medicion(id_medicion, datos)
        return {
            "mensaje": "Medición actualizada correctamente",
            "datos": convertir_a_dict(dato)
        }
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.delete("/mediciones/{id_medicion}")
def eliminar_medicion(
    id_medicion: int,
    db: Session = Depends(get_db)
):
    service = MedicionService(db)
    try:
        service.eliminar_medicion(id_medicion)
        return {"mensaje": "Medición eliminada correctamente"}
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
