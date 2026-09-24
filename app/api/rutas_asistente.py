from typing import Any, Dict
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.asistente_google import AsistenteGoogleService

router = APIRouter(
    prefix="/agua",
    tags=["Asistente de Google"]
)

@router.post("/asistente-google")
def webhook_asistente_google(
    payload: Dict[str, Any],
    response: Response,
    db: Session = Depends(get_db)
):
    # Omitir la pantalla de advertencia de ngrok
    response.headers["ngrok-skip-browser-warning"] = "true"
    
    servicio = AsistenteGoogleService(db)
    return servicio.procesar_peticion(payload)