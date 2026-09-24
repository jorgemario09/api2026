from app.repositories.base_repository import BaseRepository
from app.models.umbral import Umbral


class UmbralRepository(BaseRepository):

    def obtener_umbrales(self):
        return self.obtener_todos(Umbral)

    def obtener_umbral(self, id_umbral: int):
        return self.obtener_por_id(Umbral, "id_umbral", id_umbral)

    def crear_umbral(self, datos: dict):
        return self.crear(Umbral, datos)

    def actualizar_umbral(self, id_umbral: int, datos: dict):
        return self.actualizar(Umbral, "id_umbral", id_umbral, datos)

    def eliminar_umbral(self, id_umbral: int):
        return self.eliminar(Umbral, "id_umbral", id_umbral)