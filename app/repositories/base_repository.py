from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


class BaseRepository:
    """
    Clase base con métodos CRUD genéricos y manejo de transacciones.
    """

    def __init__(self, db: Session):
        self.db = db

    def crear(self, modelo, datos: dict):
        try:
            objeto = modelo(**datos)
            self.db.add(objeto)
            self.db.commit()
            self.db.refresh(objeto)
            return objeto
        except SQLAlchemyError as error:
            self.db.rollback()
            raise error

    def obtener_todos(self, modelo):
        return self.db.query(modelo).all()

    def obtener_por_id(self, modelo, nombre_id: str, valor_id: int):
        return (
            self.db
            .query(modelo)
            .filter(getattr(modelo, nombre_id) == valor_id)
            .first()
        )

    def actualizar(self, modelo, nombre_id: str, valor_id: int, datos: dict):
        try:
            objeto = self.obtener_por_id(modelo, nombre_id, valor_id)
            if objeto is None:
                return None

            for campo, valor in datos.items():
                if hasattr(objeto, campo):
                    setattr(objeto, campo, valor)

            self.db.commit()
            self.db.refresh(objeto)
            return objeto
        except SQLAlchemyError as error:
            self.db.rollback()
            raise error

    def eliminar(self, modelo, nombre_id: str, valor_id: int):
        try:
            objeto = self.obtener_por_id(modelo, nombre_id, valor_id)
            if objeto is None:
                return None

            self.db.delete(objeto)
            self.db.commit()
            return True
        except SQLAlchemyError as error:
            self.db.rollback()
            raise error