from app.services.base_service import BaseService
from app.repositories.sensor import SensorRepository


class SensorService(BaseService):

    def __init__(self, db):
        self.repository = SensorRepository(db)

    def listar_sensores(self):
        return self.repository.obtener_sensores()

    def obtener_sensor(self, id_sensor):
        resultado = self.repository.obtener_sensor(id_sensor)
        if resultado is None:
            raise ValueError("El sensor no existe")
        return resultado

    def crear_sensor(self, datos):
        self.validar_datos(datos)
        campos_obligatorios = [
            "codigo_sensor", "id_tipo_sensor", "id_tipo_medicion",
            "id_dispositivo", "fecha_instalacion"
        ]
        for campo in campos_obligatorios:
            if not datos.get(campo):
                raise ValueError(f"El campo {campo} es obligatorio")
        return self.repository.crear_sensor(datos)

    def actualizar_sensor(self, id_sensor, datos):
        resultado = self.repository.actualizar_sensor(id_sensor, datos)
        if resultado is None:
            raise ValueError("El sensor no existe")
        return resultado

    def eliminar_sensor(self, id_sensor):
        resultado = self.repository.eliminar_sensor(id_sensor)
        if resultado is None:
            raise ValueError("El sensor no existe")
        return resultado