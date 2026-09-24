from fastapi import FastAPI
from app.api import router as api_router

app = FastAPI(
    title="API Sistema de Monitoreo de Agua",
    description=(
        "API REST para la gestión de sensores, "
        "mediciones, dispositivos, eventos y "
        "demás información del sistema de monitoreo de agua."
    ),
    version="1.0.0"
)

# Registrar los 11 routers correspondientes a las tablas de la base de datos
app.include_router(api_router)


@app.get("/", tags=["Inicio"])
def inicio():
    return {
        "mensaje": "API del Sistema de Monitoreo de Agua funcionando",
        "version": "1.0.0",
        "estado": "ONLINE"
    }


@app.get("/health", tags=["Sistema"])
def health_check():
    return {
        "estado": "OK",
        "mensaje": "La API está funcionando correctamente"
    }