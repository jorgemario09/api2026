import os
from fastapi import APIRouter, File, UploadFile, HTTPException
import ultralytics
import cv2
import numpy as np

router = APIRouter(
    prefix="/agua",
    tags=["Visión Artificial (YOLO)"]
)

# Buscar el archivo .pt dentro de tu proyecto (app/weights/best.pt)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, "app", "weights", "best.pt")

model = None
try:
    if os.path.exists(MODEL_PATH):
        model = ultralytics.YOLO(MODEL_PATH)
    else:
        print(f"Advertencia: No se encontró el modelo YOLO en {MODEL_PATH}")
except Exception as e:
    print(f"Error al cargar el modelo YOLO: {e}")

@router.post("/inferencia-yolo")
async def ejecutar_inferencia(file: UploadFile = File(...)):
    if model is None:
        raise HTTPException(
            status_code=500, 
            detail="El modelo YOLO no está cargado en el servidor. Verifica que 'best.pt' esté subido en 'app/weights/'."
        )
    
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        raise HTTPException(status_code=400, detail="El archivo enviado no es una imagen válida.")

    results = model(img)
    
    detecciones = []
    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            xyxy = box.xyxy[0].tolist()
            clase_nombre = model.names[cls_id]
            
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