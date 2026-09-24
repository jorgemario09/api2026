from app.repositories.base_repository import BaseRepository
from app.models.tipo_sensor import TipoSensor


class TipoSensorRepository(BaseRepository):

    def obtener_tipos_sensor(self):
        return self.obtener_todos(TipoSensor)

    def obtener_tipo_sensor(self, id_tipo_sensor: int):
        return self.obtener_por_id(TipoSensor, "id_tipo_sensor", id_tipo_sensor)

    def crear_tipo_sensor(self, datos: dict):
        return self.crear(TipoSensor, datos)

    def actualizar_tipo_sensor(self, id_tipo_sensor: int, datos: dict):
        return self.actualizar(TipoSensor, "id_tipo_sensor", id_tipo_sensor, datos)

    def eliminar_tipo_sensor(self, id_tipo_sensor: int):
        return self.eliminar(TipoSensor, "id_tipo_sensor", id_tipo_sensor)