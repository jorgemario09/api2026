import time
import os
import subprocess
import requests
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

API_URL = "http://localhost:8000/agua/whatsapp"

def iniciar_bot():
    print("Iniciando Google Chrome...")
    
    session_dir = os.path.abspath("./session_whatsapp_v3")
    if not os.path.exists(session_dir):
        os.makedirs(session_dir)

    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if not os.path.exists(chrome_path):
        chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

    cmd = f'"{chrome_path}" --remote-debugging-port=9222 --user-data-dir="{session_dir}" https://web.whatsapp.com'
    subprocess.Popen(cmd, shell=True)
    
    time.sleep(3)

    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        print("✅ Conexión con Chrome establecida con éxito.")
    except Exception as e:
        print(f"\n❌ Error al conectar Selenium: {e}")
        return

    print("\n1. Escanea el código QR en Chrome si es necesario.")
    print("2. Abre el CHAT de prueba en WhatsApp Web.")
    
    input("\n👉 Presiona ENTER aquí en la terminal cuando estés dentro del CHAT...")

    # --- CALIBRACIÓN INICIAL: Ignorar mensajes que ya estaban en pantalla ---
    print("⏳ Registrando estado actual del chat...")
    elementos_inicio = driver.find_elements(By.XPATH, '//span[@dir="ltr"]')
    if not elementos_inicio:
        elementos_inicio = driver.find_elements(By.XPATH, '//div[contains(@class, "message-in")]//span')

    ultimo_mensaje_procesado = ""
    if elementos_inicio:
        textos_inicio = [e.text.strip() for e in elementos_inicio if e.text.strip()]
        if textos_inicio:
            ultimo_mensaje_procesado = textos_inicio[-1]
            print(f"📌 Último texto antiguo ignorado: '{ultimo_mensaje_procesado}'")

    print("✅ BOT ACTIVO. Esperando que envíes un NUEVO mensaje desde el celular...")

    # --- BUCLE PRINCIPAL DE ESCUCHA ---
    while True:
        try:
            elementos_texto = driver.find_elements(
                By.XPATH, 
                '//div[contains(@class, "message-in")]//span[contains(@class, "selectable-text")]'
            )

            if not elementos_texto:
                elementos_texto = driver.find_elements(By.XPATH, '//span[@dir="ltr"]')

            if elementos_texto:
                textos = [elem.text.strip() for elem in elementos_texto if elem.text.strip()]
                
                if textos:
                    texto_recibido = textos[-1]

                    # 1. Verificar si es un texto verdaderamente NUEVO
                    if texto_recibido and texto_recibido != ultimo_mensaje_procesado:
                        
                        # 2. ANTIBUCLE: Ignorar si el texto detectado es una respuesta propia del bot
                        respuestas_bot_prefijos = (
                            "El promedio", "Se encontraron", "La ultima", 
                            "Actualmente", "Hola", "Error"
                        )
                        
                        if any(texto_recibido.startswith(prefix) for prefix in respuestas_bot_prefijos):
                            # Actualizar memoria sin responder para romper cualquier bucle
                            ultimo_mensaje_procesado = texto_recibido
                            continue

                        print(f"\n📩 NUEVO mensaje detectado: '{texto_recibido}'")
                        ultimo_mensaje_procesado = texto_recibido

                        # 3. Consultar a la API
                        try:
                            res = requests.post(API_URL, json={"mensaje": texto_recibido}, timeout=5)
                            if res.status_code == 200:
                                respuesta = res.json().get("respuesta", "Sin respuesta.")
                            else:
                                respuesta = "Error al consultar la base de datos."
                        except Exception as err:
                            respuesta = f"Error al conectar con la API: {err}"

                        # 4. Enviar respuesta a la casilla editable
                        cajas = driver.find_elements(By.XPATH, '//div[@contenteditable="true"]')
                        if cajas:
                            caja = cajas[-1]
                            caja.click()
                            time.sleep(0.3)
                            pyperclip.copy(respuesta)
                            caja.send_keys(Keys.CONTROL, 'v')
                            time.sleep(0.3)
                            caja.send_keys(Keys.ENTER)
                            
                            print(f"🤖 Respuesta enviada: '{respuesta}'")
                            
                            # Guardar la respuesta enviada en memoria para reforzar la protección antibucle
                            time.sleep(1)
                            ultimo_mensaje_procesado = respuesta

            time.sleep(2)

        except KeyboardInterrupt:
            print("\nBot detenido.")
            break
        except Exception:
            time.sleep(2)

if __name__ == "__main__":
    iniciar_bot()