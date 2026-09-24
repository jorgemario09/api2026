from app.repositories.base_repository import BaseRepository
from app.models.medicion import Medicion
from app.models.vw_medicion_optimizada import VwMedicionOptimizada


class MedicionRepository(BaseRepository):

    def obtener_mediciones(self):
        # Mantiene la consulta a la vista optimizada[cite: 3]
        return self.obtener_todos(VwMedicionOptimizada)

    def obtener_medicion(self, id_medicion: int):
        return self.obtener_por_id(Medicion, "id_medicion", id_medicion)

    def crear_medicion(self, datos: dict):
        return self.crear(Medicion, datos)

    def actualizar_medicion(self, id_medicion: int, datos: dict):
        return self.actualizar(Medicion, "id_medicion", id_medicion, datos)

    def eliminar_medicion(self, id_medicion: int):
        return self.eliminar(Medicion, "id_medicion", id_medicion)