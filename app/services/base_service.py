class BaseService:
    """
    Clase base para todos los servicios del dominio.
    Contiene métodos auxiliares y validaciones compartidas.
    """

    def validar_datos(self, datos):
        if not isinstance(datos, dict):
            raise ValueError("Los datos deben enviarse como un objeto JSON")
        return True