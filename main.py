from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <-- Importante para peticiones desde App Móvil / Web
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

# Configuración Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite peticiones desde cualquier origen (móvil, web local o Render)
    allow_credentials=True,
    allow_methods=["*"],  # Permite GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],
)

# Registrar routers (incluye mediciones, dispositivos y el nuevo de predicción ML)
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
