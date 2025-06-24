import time
import cv2
from ultralytics import YOLO
from pathlib import Path

# 1. Carga modelo
model = YOLO('yolov8n.pt')

# 2. Configuración
img_path = r'C:\Users\Alex2\Desktop\YOLO\image\imagen.jpg'
imgsz = 320

# 3. Inferencia y medición
start = time.time()
results = model.predict(source=img_path, imgsz=imgsz, device='cpu')
end = time.time()
print(f"Inferencia total: {end - start:.2f} s en {imgsz}x{imgsz}")

# 4. Mostrar detecciones por consola
for r in results:
    for box in r.boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        conf = float(box.conf[0])
        cls_id = int(box.cls[0])
        label = model.names[cls_id]
        print(f"  - {label}, conf={conf:.2f}, bbox={[x1, y1, x2, y2]}")

# 5. Mostrar la imagen anotada
annotated = results[0].plot()
cv2.imshow('Detecciones YOLOv8', annotated)
cv2.waitKey(0)
cv2.destroyAllWindows()
