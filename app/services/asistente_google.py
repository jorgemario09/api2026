from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.medicion import Medicion
from app.models.sensor import Sensor
from app.models.tipo_sensor import TipoSensor

class AsistenteGoogleService:
    """
    Servicio encargado de procesar la intencionalidad proveniente de Dialogflow
    y realizar las consultas correspondientes a la base de datos Neon.
    """
    def __init__(self, db: Session):
        self.db = db

    def procesar_peticion(self, req_data: dict) -> dict:
        # Extraer el nombre de la intencionalidad (Intent) identificada por Dialogflow
        intent_name = (
            req_data.get("queryResult", {})
            .get("intent", {})
            .get("displayName", "")
        )

        # 1. "dame el ultimo valor del sensor"
        if intent_name == "ObtenerUltimoValor":
            medicion = (
                self.db.query(Medicion)
                .order_by(Medicion.fecha_hora.desc())
                .first()
            )
            if medicion:
                texto_respuesta = (
                    f"El último valor registrado por el sistema es {float(medicion.valor):.2f} "
                    f"con fecha {medicion.fecha_hora.strftime('%d/%m/%Y %H:%M')}."
                )
            else:
                texto_respuesta = "No hay mediciones registradas en la base de datos."

        # 2. "dame el promedio de la medicion"
        elif intent_name == "ObtenerPromedio":
            promedio = self.db.query(func.avg(Medicion.valor)).scalar()
            if promedio is not None:
                texto_respuesta = (
                    f"El promedio general de las mediciones del sistema es {float(promedio):.2f}."
                )
            else:
                texto_respuesta = "No se pudieron calcular promedios porque no existen mediciones."

        # 3. "dame el nombre del sensor"
        elif intent_name == "ObtenerNombreSensor":
            sensor = self.db.query(Sensor).first()
            if sensor:
                tipo = self.db.query(TipoSensor).filter_by(id_tipo_sensor=sensor.id_tipo_sensor).first()
                nombre_tipo = tipo.nombre if tipo else "Sensor de agua"
                texto_respuesta = (
                    f"El sensor registrado en el sistema es {sensor.codigo_sensor}, "
                    f"de tipo {nombre_tipo}."
                )
            else:
                texto_respuesta = "No se encontraron sensores activos en el sistema."

        # Respuesta por defecto si la intención no coincide
        else:
            texto_respuesta = "Lo siento, no tengo una respuesta configurada para esa consulta."

        # Retornar el formato exacto requerido por Dialogflow Fulfillment
        return {
            "fulfillmentText": texto_respuesta
        }