from app.services.base_service import BaseService
from app.repositories.unidad_medida import UnidadRepository


class UnidadService(BaseService):

    def __init__(self, db):
        self.repository = UnidadRepository(db)

    def listar_unidades(self):
        return self.repository.obtener_unidades()

    def obtener_unidad(self, id_unidad):
        resultado = self.repository.obtener_unidad(id_unidad)
        if resultado is None:
            raise ValueError("La unidad no existe")
        return resultado

    def crear_unidad(self, datos):
        self.validar_datos(datos)
        if not datos.get("nombre"):
            raise ValueError("El nombre es obligatorio")
        if not datos.get("simbolo"):
            raise ValueError("El símbolo es obligatorio")
        return self.repository.crear_unidad(datos)

    def actualizar_unidad(self, id_unidad, datos):
        resultado = self.repository.actualizar_unidad(id_unidad, datos)
        if resultado is None:
            raise ValueError("La unidad no existe")
        return resultado

    def eliminar_unidad(self, id_unidad):
        resultado = self.repository.eliminar_unidad(id_unidad)
        if resultado is None:
            raise ValueError("La unidad no existe")
        return resultado