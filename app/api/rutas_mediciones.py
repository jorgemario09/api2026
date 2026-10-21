from typing import Any, Dict, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.services.medicion import MedicionService
from app.models.vw_medicion_optimizada import VwMedicionOptimizada
from app.api.respuestas import convertir_a_dict, convertir_lista


router = APIRouter(
    prefix="/agua",
    tags=["Mediciones"]
)


# =========================================================
# ENDPOINTS OPTIMIZADOS PARA EL MENÚ DEL ESP32
# =========================================================

@router.get("/mediciones/promedio-24h")
def obtener_promedio_24h(db: Session = Depends(get_db)):
    """Calcula en Neon el promedio de todas las mediciones de las últimas 24 horas."""
    hace_24h = datetime.now() - timedelta(hours=24)
    resultado = db.query(func.avg(VwMedicionOptimizada.medicion)).filter(
        VwMedicionOptimizada.fecha_hora >= hace_24h
    ).scalar()
    
    promedio = round(float(resultado), 2) if resultado is not None else 0.0
    return {"promedio_24h": promedio}


@router.get("/mediciones/conteo-hoy")
def obtener_conteo_dia_actual(db: Session = Depends(get_db)):
    """Cuenta el número de registros ingresados desde la medianoche de hoy."""
    inicio_dia = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    conteo = db.query(func.count(VwMedicionOptimizada.medicion)).filter(
        VwMedicionOptimizada.fecha_hora >= inicio_dia
    ).scalar()
    
    return {"registros_hoy": conteo or 0}


@router.get("/mediciones/valores-elevados")
def obtener_valores_elevados(db: Session = Depends(get_db)):
    """Obtiene los valores máximos registrados tanto de temperatura como de turbidez."""
    max_temp = db.query(func.max(VwMedicionOptimizada.medicion)).filter(
        func.lower(VwMedicionOptimizada.tipo_medicion).like("%temp%")
    ).scalar()

    max_turb = db.query(func.max(VwMedicionOptimizada.medicion)).filter(
        func.lower(VwMedicionOptimizada.tipo_medicion).like("%turb%")
    ).scalar()

    # Si no hay distinción por tipo, toma el máximo general de la vista
    if max_temp is None and max_turb is None:
        max_general = db.query(func.max(VwMedicionOptimizada.medicion)).scalar()
        max_temp = max_general or 0.0
        max_turb = max_general or 0.0

    return {
        "max_temperatura": round(float(max_temp), 1) if max_temp is not None else 0.0,
        "max_turbidez": round(float(max_turb), 1) if max_turb is not None else 0.0
    }


# =========================================================
# MEDICIONES CONVENCIONALES CRUD
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
