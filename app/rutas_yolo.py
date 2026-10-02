from fastapi import APIRouter, File, UploadFile, HTTPException
import ultralytics
import cv2
import numpy as np

router = APIRouter(
    prefix="/agua",
    tags=["Visión Artificial (YOLO)"]
)

# Cargar el modelo entrenado (Ajusta la ruta si es necesario)
# Usamos raw string (r"") para evitar problemas con las barras invertidas en Windows
MODEL_PATH = r"C:\YOLO\runs\detect\train-2\weights\best.pt"

try:
    model = ultralytics.YOLO(MODEL_PATH)
except Exception as e:
    print(f"Error al cargar el modelo YOLO: {e}")
    model = None

@router.post("/inferencia-yolo")
async def ejecutar_inferencia(file: UploadFile = File(...)):
    if model is None:
        raise HTTPException(status_code=500, detail="El modelo YOLO no se cargó correctamente en el servidor.")
    
    # 1. Leer la imagen enviada en la petición HTTP
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        raise HTTPException(status_code=400, detail="El archivo enviado no es una imagen válida.")

    # 2. Ejecutar la inferencia
    results = model(img)
    
    # 3. Extraer los datos detectados
    detecciones = []
    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            xyxy = box.xyxy[0].tolist() # Coordenadas [x1, y1, x2, y2]
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
