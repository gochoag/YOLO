YOLOv8n + Prolog Detection Pipeline

Pasos sencillos para configurar y ejecutar el proyecto:

1. Crear entorno virtual
   Desde la raíz del proyecto, en PowerShell o CMD:
   python -m venv venv_yolo_prolog

2. Activar entorno virtual
   En PowerShell:
   .\venv_yolo_prolog\Scripts\Activate.ps1
   Si PowerShell bloquea scripts:
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   En CMD:
   venv_yolo_prolog\Scripts\activate.bat

3. Instalar dependencias
   Con el entorno activo:
   pip install -r requirements.txt
   Nota: Para PyTorch CPU-only en Windows, puede ser necesario primero:
     pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
   Luego:
     pip install -r requirements.txt

4. Verificar archivos en la raíz del proyecto
   - yolov8n.pt (~6 MB) debe estar en la carpeta principal.
   - La carpeta image/ debe existir con imágenes de prueba (por ejemplo imagen1.jpg).
   - detect.py y exportProlog.py deben estar en la raíz.

5. Ejecutar reconocimiento en una imagen
   Con el entorno activo y en la raíz del proyecto:
   python detect.py
   Esto correrá YOLOv8n sobre la imagen configurada en detect.py, mostrará en consola el tiempo y las detecciones, y abrirá una ventana con el resultado.

6. Exportar detecciones a Prolog
   Con el entorno activo y en la raíz del proyecto:
   python exportProlog.py
   Procesará todas las imágenes en image/ y generará o actualizará detections.pl con hechos Prolog:
   detected('imagen1.jpg', 'label', Xc, Yc, W, H).

7. (Opcional) Consultar en SWI-Prolog
   Abrir PowerShell en la carpeta del proyecto:
     swipl
   En el prompt de Prolog:
     ?- consult('detections.pl').
     true.
     ?- consult('logic.pl').    (si existe)
     true.
     ?- objects_in('imagen1.jpg', L).
   Salir con:
     ?- halt.

8. Añadir nuevas imágenes
   Colocar nuevos archivos en image/.
   Ejecutar de nuevo:
     python exportProlog.py
   En sesión de Prolog, recargar:
     ?- retractall(detected(_,_,_,_,_,_)).
     true.
     ?- consult('detections.pl').
     true.

9. Ajustes adicionales
   - Para cambiar la imagen en detect.py, editar la ruta img_path en el script.
   - Para modificar resolución interna, ajustar imgsz en detect.py o exportProlog.py (por ejemplo 256 o 320).
   - Si en el futuro se dispone de GPU, cambiar device='cpu' a device='cuda' en los scripts.


Con estos pasos: crear/activar venv, instalar requerimientos, ejecutar detect.py para probar una imagen, ejecutar exportProlog.py para generar detections.pl, y opcionalmente usar Prolog para consultas.
