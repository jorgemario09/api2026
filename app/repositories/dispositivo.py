from app.repositories.base_repository import BaseRepository
from app.models.dispositivo import Dispositivo


class DispositivoRepository(BaseRepository):

    def obtener_dispositivos(self):
        return self.obtener_todos(Dispositivo)

    def obtener_dispositivo(self, id_dispositivo: int):
        return self.obtener_por_id(Dispositivo, "id_dispositivo", id_dispositivo)

    def crear_dispositivo(self, datos: dict):
        return self.crear(Dispositivo, datos)

    def actualizar_dispositivo(self, id_dispositivo: int, datos: dict):
        return self.actualizar(Dispositivo, "id_dispositivo", id_dispositivo, datos)

    def eliminar_dispositivo(self, id_dispositivo: int):
        return self.eliminar(Dispositivo, "id_dispositivo", id_dispositivo)