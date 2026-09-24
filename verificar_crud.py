from collections import Counter
from sqlalchemy import inspect, text

from app.core.database import engine

# Importar los 11 modelos activos del dominio
from app.models.ubicacion import Ubicacion
from app.models.dispositivo import Dispositivo
from app.models.tipo_sensor import TipoSensor
from app.models.unidad_medida import UnidadMedida
from app.models.tipo_medicion import TipoMedicion
from app.models.sensor import Sensor
from app.models.medicion import Medicion
from app.models.tipo_evento import TipoEvento
from app.models.evento import Evento
from app.models.umbral import Umbral
from app.models.estado_dispositivo import EstadoDispositivo

from app.api import router as api_router


# ============================================================
# TABLAS ESPERADAS (11 TABLAS)
# ============================================================

MODELOS = [
    Ubicacion,
    Dispositivo,
    TipoSensor,
    UnidadMedida,
    TipoMedicion,
    Sensor,
    Medicion,
    TipoEvento,
    Evento,
    Umbral,
    EstadoDispositivo,
]


# ============================================================
# RUTAS CRUD ESPERADAS (11 ENTIDADES x 5 METODOS = 55 RUTAS)
# ============================================================

CRUD_ESPERADO = {
    "ubicaciones": "/agua/ubicaciones",
    "dispositivos": "/agua/dispositivos",
    "tipos_sensor": "/agua/tipos-sensor",
    "unidades": "/agua/unidades",
    "tipos_medicion": "/agua/tipos-medicion",
    "sensores": "/agua/sensores",
    "mediciones": "/agua/mediciones",
    "tipos_evento": "/agua/tipos-evento",
    "eventos": "/agua/eventos",
    "umbrales": "/agua/umbrales",
    "estados": "/agua/estados",
}


# ============================================================
# FUNCIONES AUXILIARES DE COMPARACIÓN
# ============================================================

def tipo_sqlalchemy(columna):
    tipo = columna.type
    nombre = type(tipo).__name__
    detalles = []

    if hasattr(tipo, "length") and tipo.length is not None:
        detalles.append(f"length={tipo.length}")
    if hasattr(tipo, "precision") and tipo.precision is not None:
        detalles.append(f"precision={tipo.precision}")
    if hasattr(tipo, "scale") and tipo.scale is not None:
        detalles.append(f"scale={tipo.scale}")

    if detalles:
        return f"{nombre}({', '.join(detalles)})"
    return nombre


def tipo_neon(columna):
    tipo = columna["type"]
    nombre = type(tipo).__name__
    detalles = []

    if hasattr(tipo, "length") and tipo.length is not None:
        detalles.append(f"length={tipo.length}")
    if hasattr(tipo, "precision") and tipo.precision is not None:
        detalles.append(f"precision={tipo.precision}")
    if hasattr(tipo, "scale") and tipo.scale is not None:
        detalles.append(f"scale={tipo.scale}")

    if detalles:
        return f"{nombre}({', '.join(detalles)})"
    return nombre


def comparar_tipo(modelo_columna, neon_columna):
    tipo_modelo = modelo_columna.type
    tipo_db = neon_columna["type"]

    familia_modelo = type(tipo_modelo).__name__.lower()
    familia_db = type(tipo_db).__name__.lower()

    equivalencias = {
        "varchar": "string",
        "text": "text",
        "integer": "integer",
        "biginteger": "biginteger",
        "bigint": "biginteger",
        "boolean": "boolean",
        "datetime": "datetime",
        "timestamp": "datetime",
        "date": "date",
        "numeric": "numeric",
    }

    familia_modelo = equivalencias.get(familia_modelo, familia_modelo)
    familia_db = equivalencias.get(familia_db, familia_db)

    if familia_modelo != familia_db:
        return False

    for atributo in ("length", "precision", "scale"):
        valor_modelo = getattr(tipo_modelo, atributo, None)
        valor_db = getattr(tipo_db, atributo, None)

        if valor_modelo is not None and valor_db is not None:
            if valor_modelo != valor_db:
                return False

    return True


# ============================================================
# 1. CONEXIÓN REAL A NEON POSTGRESQL
# ============================================================

print()
print("=" * 72)
print("  1. CONEXIÓN A NEON")
print("=" * 72)

try:
    with engine.connect() as conn:
        resultado = conn.execute(text("SELECT 1")).scalar()

    if resultado == 1:
        print("[OK] Conexión real establecida con Neon")
        print("[OK] SELECT 1 -> 1")
    else:
        print("[ERROR] SELECT 1 no devolvió 1")

except Exception as error:
    print("[ERROR] No fue posible conectar con Neon")
    print(f"        {type(error).__name__}: {error}")
    raise SystemExit(1)


# ============================================================
# 2. COMPROBACIÓN DE LAS 11 TABLAS
# ============================================================

print()
print("=" * 72)
print("  2. COMPROBACIÓN DE LAS 11 TABLAS")
print("=" * 72)

inspector = inspect(engine)
tablas_neon = set(inspector.get_table_names())

tablas_modelo = {
    modelo.__tablename__: modelo
    for modelo in MODELOS
}

tablas_faltantes = []
tablas_encontradas = []

for nombre_tabla, modelo in tablas_modelo.items():
    if nombre_tabla in tablas_neon:
        print(f"[OK]     {nombre_tabla}")
        tablas_encontradas.append(nombre_tabla)
    else:
        print(f"[FALTA]  {nombre_tabla}")
        tablas_faltantes.append(nombre_tabla)

print()
print(f"TABLAS ESPERADAS  : {len(tablas_modelo)}")
print(f"TABLAS ENCONTRADAS: {len(tablas_encontradas)}")
print(f"TABLAS FALTANTES  : {len(tablas_faltantes)}")


# ============================================================
# 3. COMPARACIÓN DE COLUMNAS (MODELOS vs NEON)
# ============================================================

print()
print("=" * 72)
print("  3. COMPARACIÓN MODELOS SQLALCHEMY vs NEON")
print("=" * 72)

errores_columnas = 0

for modelo in MODELOS:
    nombre_tabla = modelo.__tablename__

    print()
    print(f"--- {nombre_tabla} ---")

    if nombre_tabla not in tablas_neon:
        print("[OMITIDA] La tabla no existe en Neon.")
        errores_columnas += 1
        continue

    columnas_neon = {
        columna["name"]: columna
        for columna in inspector.get_columns(nombre_tabla)
    }

    columnas_modelo = {
        columna.name: columna
        for columna in modelo.__table__.columns
    }

    faltantes_en_neon = sorted(
        set(columnas_modelo) - set(columnas_neon)
    )

    extras_en_neon = sorted(
        set(columnas_neon) - set(columnas_modelo)
    )

    diferencias = []

    for nombre in faltantes_en_neon:
        print(f"[FALTA] columna en Neon: {nombre}")
        diferencias.append(nombre)

    for nombre in extras_en_neon:
        print(f"[EXTRA] columna en Neon: {nombre}")
        diferencias.append(nombre)

    for nombre in sorted(set(columnas_modelo) & set(columnas_neon)):
        columna_modelo = columnas_modelo[nombre]
        columna_neon = columnas_neon[nombre]

        tipo_modelo = tipo_sqlalchemy(columna_modelo)
        tipo_db = tipo_neon(columna_neon)

        tipo_ok = comparar_tipo(columna_modelo, columna_neon)

        nullable_modelo = bool(columna_modelo.nullable)
        nullable_db = bool(columna_neon["nullable"])

        pk_modelo = bool(columna_modelo.primary_key)
        pk_db = nombre in set(
            inspector.get_pk_constraint(nombre_tabla).get(
                "constrained_columns",
                [],
            )
        )

        if not tipo_ok:
            print(
                f"[TIPO]   {nombre}: "
                f"modelo={tipo_modelo} | Neon={tipo_db}"
            )
            diferencias.append(nombre)

        if nullable_modelo != nullable_db:
            print(
                f"[NULL]   {nombre}: "
                f"modelo={nullable_modelo} | Neon={nullable_db}"
            )
            diferencias.append(nombre)

        if pk_modelo != pk_db:
            print(
                f"[PK]     {nombre}: "
                f"modelo={pk_modelo} | Neon={pk_db}"
            )
            diferencias.append(nombre)

    if diferencias:
        errores_columnas += len(set(diferencias))
        print("[RESULTADO] DIFERENCIAS ENCONTRADAS")
    else:
        print("[RESULTADO] OK - columnas compatibles")


# ============================================================
# 4. COMPROBACIÓN DE LAS 55 RUTAS CRUD REGISTRADAS
# ============================================================

print()
print("=" * 72)
print("  4. COMPROBACIÓN DE LAS 55 RUTAS CRUD")
print("=" * 72)

rutas = [
    (
        ruta.path,
        tuple(sorted(ruta.methods or [])),
        getattr(ruta.endpoint, "__module__", ""),
        getattr(ruta.endpoint, "__name__", ""),
    )
    for ruta in api_router.routes
    if hasattr(ruta, "methods")
]

print(f"RUTAS REGISTRADAS: {len(rutas)}")

contador = Counter(
    (path, metodos)
    for path, metodos, modulo, funcion in rutas
)

duplicadas = {
    clave: cantidad
    for clave, cantidad in contador.items()
    if cantidad > 1
}

if duplicadas:
    print("[ERROR] HAY RUTAS DUPLICADAS")
    for clave, cantidad in duplicadas.items():
        print(f"        {cantidad}x {clave}")
else:
    print("[OK] No hay rutas duplicadas")


errores_crud = 0

mapa_identificadores = {
    "ubicaciones": "ubicacion",
    "dispositivos": "dispositivo",
    "tipos_sensor": "tipo_sensor",
    "unidades": "unidad",
    "tipos_medicion": "tipo_medicion",
    "sensores": "sensor",
    "mediciones": "medicion",
    "tipos_evento": "tipo_evento",
    "eventos": "evento",
    "umbrales": "umbral",
    "estados": "estado",
}

for nombre, base in CRUD_ESPERADO.items():

    rutas_tabla = [
        (path, metodos)
        for path, metodos, modulo, funcion in rutas
        if path == base or path.startswith(base + "/{")
    ]

    param_id = mapa_identificadores[nombre]
    detalle = f"{base}/{{id_{param_id}}}"

    base_metodos = set()
    detalle_metodos = set()

    for path, metodos in rutas_tabla:
        if path == base:
            base_metodos.update(metodos)
        elif path == detalle:
            detalle_metodos.update(metodos)

    base_ok = {"GET", "POST"}.issubset(base_metodos)
    detalle_ok = {"GET", "PUT", "DELETE"}.issubset(detalle_metodos)

    total_ok = base_ok and detalle_ok

    if total_ok:
        print(f"[OK]     {nombre}")
    else:
        errores_crud += 1
        print(f"[ERROR]  {nombre}")
        print(f"         Base     : {sorted(base_metodos)}")
        print(f"         Detalle  : {sorted(detalle_metodos)}")
        print(f"         Esperado base    : GET, POST")
        print(f"         Esperado detalle : GET, PUT, DELETE")


# ============================================================
# 5. RESUMEN FINAL
# ============================================================

print()
print("=" * 72)
print("  RESUMEN FINAL")
print("=" * 72)

print(f"Conexión Neon        : OK")
print(f"Tablas encontradas  : {len(tablas_encontradas)}/11")
print(f"Tablas faltantes    : {len(tablas_faltantes)}")
print(f"Diferencias columnas: {errores_columnas}")
print(f"Rutas registradas   : {len(rutas)}/55")
print(f"Rutas duplicadas    : {len(duplicadas)}")
print(f"Errores CRUD        : {errores_crud}")

print()

if (
    len(tablas_encontradas) == 11
    and not tablas_faltantes
    and errores_columnas == 0
    and len(rutas) == 55
    and not duplicadas
    and errores_crud == 0
):
    print("RESULTADO FINAL: TODO OK")
    print("No se realizaron INSERT, UPDATE ni DELETE.")
    raise SystemExit(0)

print("RESULTADO FINAL: HAY ASPECTOS QUE REVISAR")
print("No se realizaron INSERT, UPDATE ni DELETE.")
raise SystemExit(1)