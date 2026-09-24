from app.repositories.base_repository import BaseRepository
from app.models.tipo_medicion import TipoMedicion


class TipoMedicionRepository(BaseRepository):

    def obtener_tipos_medicion(self):
        return self.obtener_todos(TipoMedicion)

    def obtener_tipo_medicion(self, id_tipo_medicion: int):
        return self.obtener_por_id(TipoMedicion, "id_tipo_medicion", id_tipo_medicion)

    def crear_tipo_medicion(self, datos: dict):
        return self.crear(TipoMedicion, datos)

    def actualizar_tipo_medicion(self, id_tipo_medicion: int, datos: dict):
        return self.actualizar(TipoMedicion, "id_tipo_medicion", id_tipo_medicion, datos)

    def eliminar_tipo_medicion(self, id_tipo_medicion: int):
        return self.eliminar(TipoMedicion, "id_tipo_medicion", id_tipo_medicion)