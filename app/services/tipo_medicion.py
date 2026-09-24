from app.services.base_service import BaseService
from app.repositories.tipo_medicion import TipoMedicionRepository


class TipoMedicionService(BaseService):

    def __init__(self, db):
        self.repository = TipoMedicionRepository(db)

    def listar_tipos_medicion(self):
        return self.repository.obtener_tipos_medicion()

    def obtener_tipo_medicion(self, id_tipo_medicion):
        resultado = self.repository.obtener_tipo_medicion(id_tipo_medicion)
        if resultado is None:
            raise ValueError("El tipo de medición no existe")
        return resultado

    def crear_tipo_medicion(self, datos):
        self.validar_datos(datos)
        if not datos.get("nombre"):
            raise ValueError("El nombre es obligatorio")
        if not datos.get("id_unidad"):
            raise ValueError("Debe indicar la unidad")
        return self.repository.crear_tipo_medicion(datos)

    def actualizar_tipo_medicion(self, id_tipo_medicion, datos):
        resultado = self.repository.actualizar_tipo_medicion(id_tipo_medicion, datos)
        if resultado is None:
            raise ValueError("El tipo de medición no existe")
        return resultado

    def eliminar_tipo_medicion(self, id_tipo_medicion):
        resultado = self.repository.eliminar_tipo_medicion(id_tipo_medicion)
        if resultado is None:
            raise ValueError("El tipo de medición no existe")
        return resultado