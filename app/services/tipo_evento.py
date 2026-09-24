from app.services.base_service import BaseService
from app.repositories.tipo_evento import TipoEventoRepository


class TipoEventoService(BaseService):

    def __init__(self, db):
        self.repository = TipoEventoRepository(db)

    def listar_tipos_evento(self):
        return self.repository.obtener_tipos_evento()

    def obtener_tipo_evento(self, id_tipo_evento):
        resultado = self.repository.obtener_tipo_evento(id_tipo_evento)
        if resultado is None:
            raise ValueError("El tipo de evento no existe")
        return resultado

    def crear_tipo_evento(self, datos):
        self.validar_datos(datos)
        if not datos.get("nombre"):
            raise ValueError("El nombre es obligatorio")
        if not datos.get("nivel"):
            raise ValueError("El nivel es obligatorio")
        return self.repository.crear_tipo_evento(datos)

    def actualizar_tipo_evento(self, id_tipo_evento, datos):
        resultado = self.repository.actualizar_tipo_evento(id_tipo_evento, datos)
        if resultado is None:
            raise ValueError("El tipo de evento no existe")
        return resultado

    def eliminar_tipo_evento(self, id_tipo_evento):
        resultado = self.repository.eliminar_tipo_evento(id_tipo_evento)
        if resultado is None:
            raise ValueError("El tipo de evento no existe")
        return resultado