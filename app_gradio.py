import json
from datetime import datetime
import psycopg2
import requests
import gradio as gr
from psycopg2.extras import RealDictCursor

NEON_DB_URL = "postgresql://neondb_owner:npg_EcfluiMZ6W8z@ep-small-heart-axq4xsjf-pooler.c-4.us-east-2.aws.neon.tech/neondb?sslmode=require"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "qwen2.5:7b"

TABLAS_MAP = {
    "usuario": "usuarios",
    "persona": "usuarios",
    "medicion": "mediciones",
    "mediciones": "mediciones",
    "evento": "eventos",
    "eventos": "eventos",
    "alerta": "eventos",
    "dispositivo": "dispositivos",
    "dispositivos": "dispositivos",
    "sensor": "sensores",
    "sensores": "sensores",
    "ubicacion": "ubicaciones",
}

def responder_chat(mensaje_usuario, historial):
    if not mensaje_usuario or not mensaje_usuario.strip():
        return "", historial

    if historial is None:
        historial = []

    q = mensaje_usuario.lower()
    tabla_detectada = None

    for keyword, tabla in TABLAS_MAP.items():
        if keyword in q:
            tabla_detectada = tabla
            break

    # Construir SQL que SIEMPRE ordene por los registros más recientes
    if "promedio" in q:
        sql = "SELECT AVG(valor) AS promedio_general FROM mediciones;"
        origen_tabla = "tabla 'mediciones' (promedio)"
    elif tabla_detectada == "usuarios":
        sql = "SELECT * FROM usuarios ORDER BY id_usuario DESC LIMIT 20;"
        origen_tabla = "tabla 'usuarios'"
    elif tabla_detectada == "mediciones":
        sql = "SELECT * FROM mediciones ORDER BY fecha_hora DESC LIMIT 20;"
        origen_tabla = "tabla 'mediciones'"
    elif tabla_detectada:
        sql = f"SELECT * FROM {tabla_detectada} LIMIT 20;"
        origen_tabla = f"tabla '{tabla_detectada}'"
    else:
        sql = "SELECT * FROM vw_mediciones_optimizada ORDER BY fecha_hora DESC LIMIT 10;"
        origen_tabla = "vista 'vw_mediciones_optimizada'"

    # 1. Consulta SQL en tiempo real a Neon
    try:
        conn = psycopg2.connect(NEON_DB_URL)
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute(sql)
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        datos_db = [dict(row) for row in resultados]

    except Exception as e:
        datos_db = f"Error consultando la base de datos: {str(e)}"
        origen_tabla = "Error de SQL"

    # 2. Invocación a Ollama con timeout extendido a 120 segundos
    sys_prompt = f"""
    Eres un asistente de monitoreo de agua conectado a Neon PostgreSQL.
    Responde utilizando ÚNICAMENTE los siguientes datos extraídos en tiempo real:

    ORIGEN EN BD: {origen_tabla}
    CONSULTA SQL: {sql}
    DATOS OBTENIDOS: {json.dumps(datos_db, default=str)}

    Responde directamente a la pregunta usando estos datos exactos.
    Pregunta: {mensaje_usuario}
    """

    try:
        res = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": sys_prompt, "stream": False}, timeout=120)
        respuesta_ia = res.json().get("response", "Sin respuesta del modelo.") if res.status_code == 200 else "Error en servidor LLM."
    except Exception as err:
        respuesta_ia = f"Error de conexión: {str(err)}"

    hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    json_str = json.dumps(datos_db, indent=2, default=str)

    bloque_origen = (
        f"\n---\n📌 **Origen de Datos (Neon PostgreSQL)**\n"
        f"- **Fuente Consultada:** `{origen_tabla}`\n"
        f"- **Consulta SQL:** `{sql}`\n"
        f"- **Timestamp Consulta:** `{hora_actual}`\n\n"
        f"```json\n{json_str}\n```"
    )

    respuesta_final = f"{respuesta_ia}\n{bloque_origen}"

    historial.append({"role": "user", "content": mensaje_usuario})
    historial.append({"role": "assistant", "content": respuesta_final})

    return "", historial

css = """
body, .gradio-container { background-color: #ffffff !important; color: #171717 !important; font-family: -apple-system, sans-serif !important; }
.main, .block, .panel, .form { background-color: #ffffff !important; border: none !important; box-shadow: none !important; }
#header-title { text-align: center !important; font-size: 24px !important; font-weight: 500 !important; color: #2d3748 !important; margin-top: 40px !important; margin-bottom: 20px !important; }
.chatbot { background-color: #ffffff !important; border: none !important; max-width: 768px !important; margin: 0 auto !important; }
#input-container { max-width: 768px !important; margin: 0 auto !important; border: 1px solid #e2e8f0 !important; border-radius: 24px !important; padding: 8px 16px !important; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important; background: #ffffff !important; }
#input-container textarea { border: none !important; outline: none !important; background: transparent !important; font-size: 16px !important; }
.gr-button { background-color: #ffffff !important; color: #4a5568 !important; border: 1px solid #e2e8f0 !important; border-radius: 16px !important; }
footer { display: none !important; }
"""

with gr.Blocks(title="gradio", css=css) as demo:
    gr.Markdown("### qwen2.5:7b", elem_id="header-title")
    chatbot = gr.Chatbot(height=450, show_label=False)
    with gr.Column(elem_id="input-container"):
        msg = gr.Textbox(placeholder="¿Cómo puedo ayudarte hoy?", show_label=False, container=False)
        with gr.Row():
            btn_enviar = gr.Button("Enviar", scale=1)
            btn_limpiar = gr.Button("Limpiar", scale=1)

    msg.submit(responder_chat, [msg, chatbot], [msg, chatbot])
    btn_enviar.click(responder_chat, [msg, chatbot], [msg, chatbot])
    btn_limpiar.click(lambda: [], None, chatbot, queue=False)

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7861)