from app.repositories.base_repository import BaseRepository
from app.models.sensor import Sensor


class SensorRepository(BaseRepository):

    def obtener_sensores(self):
        return self.obtener_todos(Sensor)

    def obtener_sensor(self, id_sensor: int):
        return self.obtener_por_id(Sensor, "id_sensor", id_sensor)

    def crear_sensor(self, datos: dict):
        return self.crear(Sensor, datos)

    def actualizar_sensor(self, id_sensor: int, datos: dict):
        return self.actualizar(Sensor, "id_sensor", id_sensor, datos)

    def eliminar_sensor(self, id_sensor: int):
        return self.eliminar(Sensor, "id_sensor", id_sensor)