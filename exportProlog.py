import time
import cv2
from ultralytics import YOLO
from pathlib import Path

def export_detections_to_prolog(
    images_dir: Path,
    output_pl: Path = Path('detections.pl'),
    imgsz: int = 320,
    device: str = 'cpu'
):
   
    # Carga modelo solo una vez
    model = YOLO('yolov8n.pt')  
    # Abrir/crear el archivo de salida
    with open(output_pl, 'w', encoding='utf-8') as f:
        f.write('% Detecciones generadas automáticamente con YOLOv8n\n')
        
        img_paths = sorted(images_dir.glob('*.jpg')) + sorted(images_dir.glob('*.png'))
        if not img_paths:
            print(f"No se encontraron imágenes en {images_dir}")
        for img_path in img_paths:
            img_name = img_path.name
            # Leer la imagen
            img = cv2.imread(str(img_path))
            if img is None:
                print(f"[Advertencia] No se pudo leer {img_path}, se omite.")
                continue
                
            img_input = img

            # Inferencia
            t0 = time.time()
            results = model.predict(source=img_input, imgsz=imgsz, device=device)
            t1 = time.time()
            print(f"[Export] {img_name}: inferencia en {t1-t0:.2f}s (imgsz={imgsz})")

            # Escribir hechos Prolog
            for r in results:
                for box in r.boxes:
                    # box.xyxy: [x1,y1,x2,y2] en el espacio de la imagen pasada a inferencia
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    cls_id = int(box.cls[0])
                    label = model.names[cls_id]
                    # Calcular ancho y alto
                    w = x2 - x1
                    h = y2 - y1
                    # Escribir con dos decimales
                    fact = (
                        f"detected('{img_name}', '{label}', "
                        f"{x1:.2f}, {y1:.2f}, {w:.2f}, {h:.2f}).\n"
                    )
                    f.write(fact)
            f.write('\n')  # línea en blanco entre imágenes
    print(f"Hechos Prolog exportados en {output_pl}")

if __name__ == '__main__':
    # Definir directorio de imágenes y archivo de salida
    base_folder = Path(__file__).parent.resolve()
    images_dir = base_folder / 'image'
    output_pl = base_folder / 'detections.pl'
    # Llamar a la función
    export_detections_to_prolog(images_dir, output_pl=output_pl, imgsz=320, device='cpu')
