import os
import influxdb_client_3 as InfluxDBClient3

class InfluxService:
    def __init__(self):
        # Lee las variables desde Render o usa los valores por defecto si existen
        self.host = os.getenv("INFLUX_HOST", "http://localhost:8181")
        self.database = os.getenv("INFLUX_DATABASE", "sensores")
        self.token = os.getenv(
            "INFLUX_TOKEN", 
            "apiv3_yeF1o3TyW0VqWEYniTac1IVdXaEBs5UpbP2ykzjqGK-fQcjCWfBlpDQlnblfWdhM9v8FQ90XwjxzKR9EzTRWxA"
        )
        self.org = os.getenv("INFLUX_ORG", "iot")

    def obtener_ultimas_mediciones_mqtt(self, limite: int = 10):
        try:
            client = InfluxDBClient3.InfluxDBClient3(
                host=self.host,
                token=self.token,
                org=self.org,
                database=self.database
            )
            
            query = f"SELECT time, temp, hum FROM mqtt_consumer ORDER BY time DESC LIMIT {limite}"
            table = client.query(query=query, language="sql")
            df = table.to_pandas()
            
            if df.empty:
                return []
                
            return df.to_dict(orient="records")
        except Exception as e:
            raise ValueError(f"Error al consultar InfluxDB: {str(e)}")