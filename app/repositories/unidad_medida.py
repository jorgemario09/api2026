from app.repositories.base_repository import BaseRepository
from app.models.unidad_medida import UnidadMedida


class UnidadRepository(BaseRepository):

    def obtener_unidades(self):
        return self.obtener_todos(UnidadMedida)

    def obtener_unidad(self, id_unidad: int):
        return self.obtener_por_id(UnidadMedida, "id_unidad", id_unidad)

    def crear_unidad(self, datos: dict):
        return self.crear(UnidadMedida, datos)

    def actualizar_unidad(self, id_unidad: int, datos: dict):
        return self.actualizar(UnidadMedida, "id_unidad", id_unidad, datos)

    def eliminar_unidad(self, id_unidad: int):
        return self.eliminar(UnidadMedida, "id_unidad", id_unidad)