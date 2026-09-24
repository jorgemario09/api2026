from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.medicion import Medicion
from app.models.dispositivo import Dispositivo
from app.models.evento import Evento

class WhatsAppService:
    """
    Servicio encargado de procesar lenguaje natural desde WhatsApp
    y consultar la base de datos Neon.
    """
    def __init__(self, db: Session):
        self.db = db

    def responder_pregunta(self, texto_usuario: str) -> str:
        q = texto_usuario.lower().strip()

        # 1. Consultas sobre último valor o lectura
        if "ultimo" in q or "último" in q or "reciente" in q or "lectura" in q:
            medicion = (
                self.db.query(Medicion)
                .order_by(Medicion.fecha_hora.desc())
                .first()
            )
            if medicion:
                return (
                    f"La última medición registrada es de {float(medicion.valor):.2f} "
                    f"con calidad '{medicion.calidad_dato}' en fecha {medicion.fecha_hora.strftime('%Y-%m-%d %H:%M')}."
                )
            return "No se encontraron mediciones registradas en el sistema."

        # 2. Consultas sobre promedios
        elif "promedio" in q or "media" in q:
            promedio = self.db.query(func.avg(Medicion.valor)).scalar()
            if promedio is not None:
                return f"El promedio general de las mediciones registradas en el sistema es {float(promedio):.2f}."
            return "No hay suficientes datos para calcular el promedio."

        # 3. Consultas sobre alertas o eventos
        elif "alerta" in q or "evento" in q or "falla" in q or "problema" in q:
            eventos_activos = (
                self.db.query(Evento)
                .filter(Evento.estado == "ACTIVO")
                .all()
            )
            if eventos_activos:
                detalles = "; ".join([e.descripcion for e in eventos_activos[:3]])
                return f"Se encontraron {len(eventos_activos)} alerta(s) activa(s): {detalles}."
            return "El sistema se encuentra estable. No hay alertas activas en este momento."

        # 4. Consultas sobre dispositivos o equipos
        elif "dispositivo" in q or "equipo" in q or "sensor" in q or "tanque" in q:
            total_disp = self.db.query(Dispositivo).count()
            return f"Actualmente hay {total_disp} dispositivos registrados en la red de monitoreo."

        # Respuesta general para preguntas no mapeadas directamente
        else:
            return (
                "Hola, soy el asistente de monitoreo de agua. Puedes preguntarme en lenguaje natural sobre "
                "el último valor, el promedio de mediciones, las alertas activas o los dispositivos conectados."
            )