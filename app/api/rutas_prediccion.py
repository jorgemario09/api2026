from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/agua",
    tags=["Predicción Machine Learning"]
)

class MedicionPrediccionInput(BaseModel):
    temperatura: float
    turbidez: float

@router.post("/prediccion-calidad")
def predecir_calidad_agua(datos: MedicionPrediccionInput):
    temp = round(datos.temperatura, 1)
    turb = round(datos.turbidez, 1)

    # 1. EVALUACIÓN DINÁMICA DE LA TEMPERATURA
    if temp < 18.0:
        estado_temp = "fria"
    elif 18.0 <= temp <= 26.0:
        estado_temp = "templada (ideal)"
    elif 26.1 <= temp <= 32.0:
        estado_temp = "tibia"
    else:
        estado_temp = "caliente"

    # 2. EVALUACIÓN DINÁMICA DE LA TURBIDEZ
    if turb <= 5.0:
        estado_turb = "limpia"
    elif 5.1 <= turb <= 25.0:
        estado_turb = "moderadamente turbia"
    elif 25.1 <= turb <= 100.0:
        estado_turb = "turbia"
    else:
        estado_turb = "muy sucia/contaminada"

    # 3. DETERMINACIÓN DE CATEGORÍA DE CALIDAD Y CONFIANZA
    if turb <= 5.0 and 15.0 <= temp <= 25.0:
        categoria = "Optima"
        confianza = 98.5
        color = "#10b981"  # Verde
    elif turb <= 25.0 and temp <= 28.0:
        categoria = "Moderada"
        confianza = 94.2
        color = "#00f0ff"  # Cyan
    elif turb <= 100.0 and temp <= 32.0:
        categoria = "Turbia"
        confianza = 96.1
        color = "#f59e0b"  # Ámbar / Naranja
    else:
        categoria = "Critica"
        confianza = 99.1
        color = "#ef4444"  # Rojo

    # 4. CONSTRUCCIÓN DEL DIAGNÓSTICO DETALLADO
    diagnostico = f"El agua esta {estado_temp} ({temp}°C) y se encuentra {estado_turb} ({turb} NTU)."

    return {
        "estado": "EXITOSO",
        "temperatura_ingresada": temp,
        "turbidez_ingresada": turb,
        "categoria_predicha": categoria,
        "confianza_porcentaje": round(confianza, 1),
        "color_hex": color,
        "diagnostico": diagnostico
    }
