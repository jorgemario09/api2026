from app.services.base_service import BaseService
from app.repositories.ubicacion import UbicacionRepository


class UbicacionService(BaseService):

    def __init__(self, db):
        self.repository = UbicacionRepository(db)

    def listar_ubicaciones(self):
        return self.repository.obtener_ubicaciones()

    def obtener_ubicacion(self, id_ubicacion):
        ubicacion = self.repository.obtener_ubicacion(id_ubicacion)
        if ubicacion is None:
            raise ValueError("La ubicación no existe")
        return ubicacion

    def crear_ubicacion(self, datos):
        self.validar_datos(datos)
        if not datos.get("nombre"):
            raise ValueError("El nombre de la ubicación es obligatorio")
        return self.repository.crear_ubicacion(datos)

    def actualizar_ubicacion(self, id_ubicacion, datos):
        self.validar_datos(datos)
        ubicacion = self.repository.actualizar_ubicacion(id_ubicacion, datos)
        if ubicacion is None:
            raise ValueError("La ubicación no existe")
        return ubicacion

    def eliminar_ubicacion(self, id_ubicacion):
        resultado = self.repository.eliminar_ubicacion(id_ubicacion)
        if resultado is None:
            raise ValueError("La ubicación no existe")
        return resultado