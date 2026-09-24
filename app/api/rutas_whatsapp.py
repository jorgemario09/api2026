from typing import Any, Dict
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.whatsapp_service import WhatsAppService

router = APIRouter(
    prefix="/agua",
    tags=["WhatsApp"]
)

@router.post("/whatsapp")
def responder_whatsapp(
    payload: Dict[str, Any],
    db: Session = Depends(get_db)
):
    mensaje = payload.get("mensaje", "")
    servicio = WhatsAppService(db)
    respuesta = servicio.responder_pregunta(mensaje)
    return {
        "pregunta": mensaje,
        "respuesta": respuesta
    }