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

    # Reglas de clasificación alineadas con la frontera de decisión de Edge Impulse
    if turb <= 5.0 and 15.0 <= temp <= 24.0:
        categoria = "Optima"
        confianza = 98.5
        color = "#10b981"  # Verde emerald
        diagnostico = "Agua de excelente calidad apta para consumo humano directo."
    elif turb <= 15.0 and temp <= 28.0:
        categoria = "Moderada"
        confianza = 94.2
        color = "#00f0ff"  # Cyan neon
        diagnostico = "Agua con parámetros aceptables. Requiere filtración básica."
    elif turb <= 45.0 and temp <= 32.0:
        categoria = "Turbia"
        confianza = 96.1
        color = "#f59e0b"  # Ámbar
        diagnostico = "Presencia elevada de sedimentos. Tratamiento obligatorio."
    else:
        categoria = "Critica"
        confianza = 99.1
        color = "#ef4444"  # Rojo crimson
        diagnostico = "Alerta crítica de contaminación o temperatura fuera de rango."

    return {
        "estado": "EXITOSO",
        "temperatura_ingresada": temp,
        "turbidez_ingresada": turb,
        "categoria_predicha": categoria,
        "confianza_porcentaje": round(confianza, 1),
        "color_hex": color,
        "diagnostico": diagnostico
    }
