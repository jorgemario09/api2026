from datetime import datetime
from app.services.base_service import BaseService
from app.repositories.estado_dispositivo import EstadoRepository


class EstadoService(BaseService):

    def __init__(self, db):
        self.repository = EstadoRepository(db)

    def listar_estados(self):
        return self.repository.obtener_estados()

    def obtener_estado(self, id_estado):
        resultado = self.repository.obtener_estado(id_estado)
        if resultado is None:
            raise ValueError("El estado no existe")
        return resultado

    def crear_estado(self, datos):
        self.validar_datos(datos)
        if not datos.get("id_dispositivo"):
            raise ValueError("Debe indicar el dispositivo")
        if not datos.get("estado"):
            raise ValueError("Debe indicar el estado")
        if not datos.get("fecha_hora"):
            datos["fecha_hora"] = datetime.now()
        return self.repository.crear_estado(datos)

    def actualizar_estado(self, id_estado, datos):
        resultado = self.repository.actualizar_estado(id_estado, datos)
        if resultado is None:
            raise ValueError("El estado no existe")
        return resultado

    def eliminar_estado(self, id_estado):
        resultado = self.repository.eliminar_estado(id_estado)
        if resultado is None:
            raise ValueError("El estado no existe")
        return resultado