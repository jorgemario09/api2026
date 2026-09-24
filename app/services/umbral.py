from app.services.base_service import BaseService
from app.repositories.umbral import UmbralRepository


class UmbralService(BaseService):

    def __init__(self, db):
        self.repository = UmbralRepository(db)

    def listar_umbrales(self):
        return self.repository.obtener_umbrales()

    def obtener_umbral(self, id_umbral):
        resultado = self.repository.obtener_umbral(id_umbral)
        if resultado is None:
            raise ValueError("El umbral no existe")
        return resultado

    def crear_umbral(self, datos):
        self.validar_datos(datos)
        if not datos.get("id_tipo_medicion"):
            raise ValueError("Debe indicar el tipo de medición")
        if datos.get("valor_minimo") is None:
            raise ValueError("Debe indicar el valor mínimo")
        if datos.get("valor_maximo") is None:
            raise ValueError("Debe indicar el valor máximo")
        return self.repository.crear_umbral(datos)

    def actualizar_umbral(self, id_umbral, datos):
        resultado = self.repository.actualizar_umbral(id_umbral, datos)
        if resultado is None:
            raise ValueError("El umbral no existe")
        return resultado

    def eliminar_umbral(self, id_umbral):
        resultado = self.repository.eliminar_umbral(id_umbral)
        if resultado is None:
            raise ValueError("El umbral no existe")
        return resultado