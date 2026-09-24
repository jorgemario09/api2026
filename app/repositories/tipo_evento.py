from app.repositories.base_repository import BaseRepository
from app.models.tipo_evento import TipoEvento


class TipoEventoRepository(BaseRepository):

    def obtener_tipos_evento(self):
        return self.obtener_todos(TipoEvento)

    def obtener_tipo_evento(self, id_tipo_evento: int):
        return self.obtener_por_id(TipoEvento, "id_tipo_evento", id_tipo_evento)

    def crear_tipo_evento(self, datos: dict):
        return self.crear(TipoEvento, datos)

    def actualizar_tipo_evento(self, id_tipo_evento: int, datos: dict):
        return self.actualizar(TipoEvento, "id_tipo_evento", id_tipo_evento, datos)

    def eliminar_tipo_evento(self, id_tipo_evento: int):
        return self.eliminar(TipoEvento, "id_tipo_evento", id_tipo_evento)