import os
import gc
import traceback
from fastapi import APIRouter, File, UploadFile, HTTPException
import numpy as np

try:
    import cv2
except ModuleNotFoundError:
    cv2 = None

try:
    import torch
    import ultralytics
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
                print(f"Cargando modelo YOLO desde: {MODEL_PATH}", flush=True)
                model = ultralytics.YOLO(MODEL_PATH)
                if hasattr(model, 'eval'):
                    model.eval()
                print("Modelo YOLO cargado exitosamente.", flush=True)
            except Exception as e:
                print(f"Error cargando best.pt: {e}", flush=True)
                traceback.print_exc()
                return None, f"Error cargando best.pt: {str(e)}"
        else:
            print(f"No existe el archivo en la ruta: {MODEL_PATH}", flush=True)
            return None, f"Archivo no encontrado en servidor: {MODEL_PATH}"
            
    return model, "OK"

@router.post("/inferencia-yolo")
async def ejecutar_inferencia(file: UploadFile = File(...)):
    try:
        if cv2 is None:
            raise HTTPException(status_code=500, detail="OpenCV no está disponible.")

        yolo_model, msg_error = get_yolo_model()
        if yolo_model is None:
            raise HTTPException(status_code=500, detail=f"Modelo YOLO no disponible: {msg_error}")
        
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise HTTPException(status_code=400, detail="Imagen no válida o corrupta.")

        # Redimensionar para reducir consumo de RAM
        img_resized = cv2.resize(img, (256, 256))

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
        
        del img, img_resized, results
        gc.collect()

        return {
            "estado": "EXITOSO",
            "total_detectados": len(detecciones),
            "detecciones": detecciones
        }

    except HTTPException:
        raise
    except Exception as e:
        print("--- ERROR EN INFERENCIA YOLO ---", flush=True)
        traceback.print_exc()
        gc.collect()
        raise HTTPException(status_code=500, detail=f"Error en servidor: {str(e)}")