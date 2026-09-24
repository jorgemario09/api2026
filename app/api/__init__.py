from fastapi import APIRouter

from app.api.rutas_ubicaciones import router as ubicaciones_router
from app.api.rutas_dispositivos import router as dispositivos_router
from app.api.rutas_tipos_sensor import router as tipos_sensor_router
from app.api.rutas_unidades import router as unidades_router
from app.api.rutas_tipos_medicion import router as tipos_medicion_router
from app.api.rutas_sensores import router as sensores_router
from app.api.rutas_mediciones import router as mediciones_router
from app.api.rutas_tipos_evento import router as tipos_evento_router
from app.api.rutas_eventos import router as eventos_router
from app.api.rutas_umbrales import router as umbrales_router
from app.api.rutas_estados import router as estados_router
from app.api.rutas_asistente import router as asistente_router
from app.api.rutas_whatsapp import router as whatsapp_router
router = APIRouter()

router.routes.extend(ubicaciones_router.routes)
router.routes.extend(dispositivos_router.routes)
router.routes.extend(tipos_sensor_router.routes)
router.routes.extend(unidades_router.routes)
router.routes.extend(tipos_medicion_router.routes)
router.routes.extend(sensores_router.routes)
router.routes.extend(mediciones_router.routes)
router.routes.extend(tipos_evento_router.routes)
router.routes.extend(eventos_router.routes)
router.routes.extend(umbrales_router.routes)
router.routes.extend(estados_router.routes)
router.routes.extend(asistente_router.routes)
router.routes.extend(whatsapp_router.routes)