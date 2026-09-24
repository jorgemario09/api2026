def convertir_a_dict(objeto):
    if objeto is None:
        return None

    datos = {}

    # Soporte para Vistas Mapeadas en SQLAlchemy
    if hasattr(objeto, "__mapper__"):
        for columna in objeto.__mapper__.columns:
            datos[columna.key] = getattr(objeto, columna.key)

    # Soporte para Tablas Físicas Convencionales
    elif hasattr(objeto, "__table__"):
        for columna in objeto.__table__.columns:
            datos[columna.name] = getattr(objeto, columna.name)

    return datos


def convertir_lista(lista):
    return [
        convertir_a_dict(objeto)
        for objeto in lista
    ]