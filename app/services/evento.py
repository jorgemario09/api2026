from datetime import datetime
from app.services.base_service import BaseService
from app.repositories.evento import EventoRepository


class EventoService(BaseService):

    def __init__(self, db):
        self.repository = EventoRepository(db)

    def listar_eventos(self):
        return self.repository.obtener_eventos()

    def obtener_evento(self, id_evento):
        resultado = self.repository.obtener_evento(id_evento)
        if resultado is None:
            raise ValueError("El evento no existe")
        return resultado

    def crear_evento(self, datos):
        self.validar_datos(datos)
        if not datos.get("id_tipo_evento"):
            raise ValueError("Debe indicar el tipo de evento")
        if not datos.get("id_dispositivo"):
            raise ValueError("Debe indicar el dispositivo")
        if not datos.get("fecha_hora"):
            datos["fecha_hora"] = datetime.now()
        if not datos.get("estado"):
            datos["estado"] = "ACTIVO"
        return self.repository.crear_evento(datos)

    def actualizar_evento(self, id_evento, datos):
        resultado = self.repository.actualizar_evento(id_evento, datos)
        if resultado is None:
            raise ValueError("El evento no existe")
        return resultado

    def eliminar_evento(self, id_evento):
        resultado = self.repository.eliminar_evento(id_evento)
        if resultado is None:
            raise ValueError("El evento no existe")
        return resultado