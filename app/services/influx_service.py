import os
import influxdb_client_3 as InfluxDBClient3

class InfluxService:
    def __init__(self):
        self.host = "http://localhost:8181"
        self.database = "sensores"
        # En InfluxDB 3 local con quick-start, a veces se usa una cadena vacía o un token por defecto si la auth estricta no está mapeada al cliente Python
        self.token = "apiv3_yeF1o3TyW0VqWEYniTac1IVdXaEBs5UpbP2ykzjqGK-fQcjCWfBlpDQlnblfWdhM9v8FQ90XwjxzKR9EzTRWxA" 
        self.org = "iot"

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