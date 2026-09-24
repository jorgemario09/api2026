from app.services.base_service import BaseService
from app.repositories.tipo_sensor import TipoSensorRepository


class TipoSensorService(BaseService):

    def __init__(self, db):
        self.repository = TipoSensorRepository(db)

    def listar_tipos_sensor(self):
        return self.repository.obtener_tipos_sensor()

    def obtener_tipo_sensor(self, id_tipo_sensor):
        resultado = self.repository.obtener_tipo_sensor(id_tipo_sensor)
        if resultado is None:
            raise ValueError("El tipo de sensor no existe")
        return resultado

    def crear_tipo_sensor(self, datos):
        self.validar_datos(datos)
        if not datos.get("nombre"):
            raise ValueError("El nombre es obligatorio")
        return self.repository.crear_tipo_sensor(datos)

    def actualizar_tipo_sensor(self, id_tipo_sensor, datos):
        resultado = self.repository.actualizar_tipo_sensor(id_tipo_sensor, datos)
        if resultado is None:
            raise ValueError("El tipo de sensor no existe")
        return resultado

    def eliminar_tipo_sensor(self, id_tipo_sensor):
        resultado = self.repository.eliminar_tipo_sensor(id_tipo_sensor)
        if resultado is None:
            raise ValueError("El tipo de sensor no existe")
        return resultado