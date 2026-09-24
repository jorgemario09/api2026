from app.repositories.base_repository import BaseRepository
from app.models.evento import Evento


class EventoRepository(BaseRepository):

    def obtener_eventos(self):
        return self.obtener_todos(Evento)

    def obtener_evento(self, id_evento: int):
        return self.obtener_por_id(Evento, "id_evento", id_evento)

    def crear_evento(self, datos: dict):
        return self.crear(Evento, datos)

    def actualizar_evento(self, id_evento: int, datos: dict):
        return self.actualizar(Evento, "id_evento", id_evento, datos)

    def eliminar_evento(self, id_evento: int):
        return self.eliminar(Evento, "id_evento", id_evento)