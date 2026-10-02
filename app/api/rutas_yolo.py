import os
import gc
from fastapi import APIRouter, File, UploadFile, HTTPException
import numpy as np

try:
    import cv2
except ModuleNotFoundError:
    cv2 = None

try:
    import torch
    import ultralytics
    # Desactivar autograd para reducir consumo de memoria global
    torch.set_grad_enabled(False)
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
    if ultralytics is None or torch is None:
        return None, "Librerías PyTorch/Ultralytics no disponibles."
        
    if model is None:
        if os.path.exists(MODEL_PATH):
            try:
                # Cargar modelo directamente en CPU
                model = ultralytics.YOLO(MODEL_PATH)
                if hasattr(model, 'eval'):
                    model.eval()
            except Exception as e:
                return None, f"Error cargando best.pt: {str(e)}"
        else:
            return None, f"No se encontró el archivo en {MODEL_PATH}"
            
    return model, "OK"

@router.post("/inferencia-yolo")
async def ejecutar_inferencia(file: UploadFile = File(...)):
    if cv2 is None:
        raise HTTPException(status_code=500, detail="OpenCV no instalado.")

    yolo_model, msg_error = get_yolo_model()
    if yolo_model is None:
        raise HTTPException(status_code=500, detail=f"Modelo no disponible: {msg_error}")
    
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        raise HTTPException(status_code=400, detail="Imagen no válida.")

    # Redimensionar la imagen a un tamaño pequeño (256x256 o 320x320)
    # Esto evita picos de uso de RAM en la matriz de la imagen
    img_resized = cv2.resize(img, (256, 256))

    try:
        # Inferencia rápida sin rastreo de gradientes
        with torch.no_grad():
            results = yolo_model(img_resized, imgsz=256, verbose=False)
        
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
        
        # Limpieza forzada de basura en memoria tras la inferencia
        del img, img_resized, results
        gc.collect()

        return {
            "estado": "EXITOSO",
            "total_detectados": len(detecciones),
            "detecciones": detecciones
        }
    except Exception as e:
        gc.collect()
        raise HTTPException(status_code=500, detail=f"Error durante inferencia: {str(e)}")