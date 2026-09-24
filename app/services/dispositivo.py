from datetime import datetime
from app.services.base_service import BaseService
from app.repositories.dispositivo import DispositivoRepository


class DispositivoService(BaseService):

    def __init__(self, db):
        self.repository = DispositivoRepository(db)

    def listar_dispositivos(self):
        return self.repository.obtener_dispositivos()

    def obtener_dispositivo(self, id_dispositivo):
        dispositivo = self.repository.obtener_dispositivo(id_dispositivo)
        if dispositivo is None:
            raise ValueError("El dispositivo no existe")
        return dispositivo

    def crear_dispositivo(self, datos):
        self.validar_datos(datos)
        if not datos.get("nombre"):
            raise ValueError("El nombre del dispositivo es obligatorio")
        if not datos.get("codigo"):
            raise ValueError("El código del dispositivo es obligatorio")
        if not datos.get("id_ubicacion"):
            raise ValueError("Debe indicar la ubicación")
        if not datos.get("fecha_registro"):
            datos["fecha_registro"] = datetime.now()
        return self.repository.crear_dispositivo(datos)

    def actualizar_dispositivo(self, id_dispositivo, datos):
        self.validar_datos(datos)
        dispositivo = self.repository.actualizar_dispositivo(id_dispositivo, datos)
        if dispositivo is None:
            raise ValueError("El dispositivo no existe")
        return dispositivo

    def eliminar_dispositivo(self, id_dispositivo):
        resultado = self.repository.eliminar_dispositivo(id_dispositivo)
        if resultado is None:
            raise ValueError("El dispositivo no existe")
        return resultado