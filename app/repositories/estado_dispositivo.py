from app.repositories.base_repository import BaseRepository
from app.models.estado_dispositivo import EstadoDispositivo


class EstadoRepository(BaseRepository):

    def obtener_estados(self):
        return self.obtener_todos(EstadoDispositivo)

    def obtener_estado(self, id_estado: int):
        return self.obtener_por_id(EstadoDispositivo, "id_estado", id_estado)

    def crear_estado(self, datos: dict):
        return self.crear(EstadoDispositivo, datos)

    def actualizar_estado(self, id_estado: int, datos: dict):
        return self.actualizar(EstadoDispositivo, "id_estado", id_estado, datos)

    def eliminar_estado(self, id_estado: int):
        return self.eliminar(EstadoDispositivo, "id_estado", id_estado)