from app.repositories.base_repository import BaseRepository
from app.models.ubicacion import Ubicacion


class UbicacionRepository(BaseRepository):

    def obtener_ubicaciones(self):
        return self.obtener_todos(Ubicacion)

    def obtener_ubicacion(self, id_ubicacion: int):
        return self.obtener_por_id(Ubicacion, "id_ubicacion", id_ubicacion)

    def crear_ubicacion(self, datos: dict):
        return self.crear(Ubicacion, datos)

    def actualizar_ubicacion(self, id_ubicacion: int, datos: dict):
        return self.actualizar(Ubicacion, "id_ubicacion", id_ubicacion, datos)

    def eliminar_ubicacion(self, id_ubicacion: int):
        return self.eliminar(Ubicacion, "id_ubicacion", id_ubicacion)