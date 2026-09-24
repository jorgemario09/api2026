from datetime import datetime
from app.services.base_service import BaseService
from app.repositories.medicion import MedicionRepository


class MedicionService(BaseService):

    def __init__(self, db):
        self.repository = MedicionRepository(db)

    def listar_mediciones(self):
        return self.repository.obtener_mediciones()

    def obtener_medicion(self, id_medicion):
        resultado = self.repository.obtener_medicion(id_medicion)
        if resultado is None:
            raise ValueError("La medición no existe")
        return resultado

    def crear_medicion(self, datos):
        self.validar_datos(datos)
        if not datos.get("id_sensor"):
            raise ValueError("Debe indicar el sensor")
        if datos.get("valor") is None:
            raise ValueError("El valor de la medición es obligatorio")
        if not datos.get("fecha_hora"):
            datos["fecha_hora"] = datetime.now()
        if not datos.get("calidad_dato"):
            datos["calidad_dato"] = "VALIDO"
        return self.repository.crear_medicion(datos)

    def actualizar_medicion(self, id_medicion, datos):
        resultado = self.repository.actualizar_medicion(id_medicion, datos)
        if resultado is None:
            raise ValueError("La medición no existe")
        return resultado

    def eliminar_medicion(self, id_medicion):
        resultado = self.repository.eliminar_medicion(id_medicion)
        if resultado is None:
            raise ValueError("La medición no existe")
        return resultado