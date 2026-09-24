#database

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv


# =========================================================
# CARGAR VARIABLES DEL ARCHIVO .env
# =========================================================

load_dotenv()


# =========================================================
# URL DE CONEXIÓN A POSTGRESQL
# =========================================================

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "No se encontró DATABASE_URL en el archivo .env"
    )


# =========================================================
# MOTOR DE BASE DE DATOS
# =========================================================

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)


# =========================================================
# FÁBRICA DE SESIONES
# =========================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# =========================================================
# CLASE BASE PARA LOS MODELOS
# =========================================================

Base = declarative_base()


# =========================================================
# OBTENER SESIÓN DE BASE DE DATOS
# =========================================================

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()