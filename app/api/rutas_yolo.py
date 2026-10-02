import os
import numpy as np
import cv2
from fastapi import APIRouter, File, UploadFile, HTTPException

# Importación segura de PyTorch y Ultralytics
try:
    import torch
    import ultralytics
except ModuleNotFoundError:
    torch = None
    ultralytics = None

router = APIRouter(
    prefix="/agua",
    tags=["Visión Artificial (YOLO)"]
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, "app", "weights", "best.pt")

model = None

def get_yolo_model():
    global model
    if torch is None or ultralytics is None:
        print("Advertencia: PyTorch o Ultralytics no están instalados en este entorno.")
        return None
        
    if model is None:
        if os.path.exists(MODEL_PATH):
            try:
                model = ultralytics.YOLO(MODEL_PATH)
            except Exception as e:
                print(f"Error al cargar el modelo YOLO: {e}")
                return None
        else:
            print(f"No se encontró el archivo de pesos en: {MODEL_PATH}")
            return None
    return model

@router.post("/inferencia-yolo")
async def ejecutar_inferencia(file: UploadFile = File(...)):
    yolo_model = get_yolo_model()
    if yolo_model is None:
        raise HTTPException(
            status_code=500, 
            detail="El modelo YOLO o PyTorch no está disponible en el servidor de Render."
        )
    
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        raise HTTPException(status_code=400, detail="Imagen no válida.")

    img_resized = cv2.resize(img, (320, 320))

    with torch.no_grad():
        results = yolo_model(img_resized, imgsz=320)
    
    detecciones = []
    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            xyxy = box.xyxy[0].tolist()
            clase_nombre = yolo_model.names[cls_id]
            
            detecciones.append({
                "clase": clase_nombre,
                "confianza": round(conf * 100, 2),
                "bounding_box": [round(coord, 2) for coord in xyxy]
            })
            
    return {
        "estado": "EXITOSO",
        "total_detectados": len(detecciones),
        "detecciones": detecciones
    }