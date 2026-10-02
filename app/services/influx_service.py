import os

# Importación defensiva de InfluxDB para evitar caídas en entornos de producción (Render)
try:
    import influxdb_client_3 as InfluxDBClient3
except ModuleNotFoundError:
    try:
        import influxdb_client as InfluxDBClient3
    except ModuleNotFoundError:
        InfluxDBClient3 = None


class InfluxService:
    def __init__(self):
        self.host = os.getenv("INFLUX_HOST", "http://localhost:8181")
        self.database = os.getenv("INFLUX_DATABASE", "sensores")
        self.token = os.getenv("INFLUX_TOKEN", "")
        self.org = os.getenv("INFLUX_ORG", "iot")

    def obtener_ultimas_mediciones_mqtt(self, limite: int = 10):
        # Si la librería no está disponible en el servidor, retorna lista vacía en lugar de crash
        if InfluxDBClient3 is None:
            print("Advertencia: Módulo de InfluxDB no disponible en este entorno.")
            return []
            
        try:
            # Detección dinámica de la API del cliente (v3 o v2/v1)
            if hasattr(InfluxDBClient3, "InfluxDBClient3"):
                client = InfluxDBClient3.InfluxDBClient3(
                    host=self.host,
                    token=self.token,
                    org=self.org,
                    database=self.database
                )
            else:
                client = InfluxDBClient3.InfluxDBClient(
                    url=self.host,
                    token=self.token,
                    org=self.org
                )
                
            query = f"SELECT time, temp, hum FROM mqtt_consumer ORDER BY time DESC LIMIT {limite}"
            table = client.query(query=query, language="sql")
            df = table.to_pandas()

            if df.empty:
                return []

            return df.to_dict(orient="records")
            
        except Exception as e:
            print(f"Advertencia al consultar InfluxDB: {str(e)}")
            return []