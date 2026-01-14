"""
Test rápido para verificar que OCR funciona
"""

import cv2
import numpy as np

try:
    import easyocr
    print("✅ EasyOCR importado correctamente")
    
    # Crear una imagen de prueba con un número
    img = np.ones((100, 200, 3), dtype=np.uint8) * 255
    cv2.putText(img, "Max: 47.1", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2)
    cv2.imwrite('/tmp/test_ocr.png', img)
    
    print("📸 Imagen de prueba creada")
    
    # Inicializar OCR
    reader = easyocr.Reader(['es', 'en'], gpu=False)
    print("✅ Reader OCR inicializado")
    
    # Leer la imagen
    resultados = reader.readtext('/tmp/test_ocr.png')
    print(f"📖 OCR resultados: {len(resultados)} elementos detectados")
    
    for i, (bbox, texto, confianza) in enumerate(resultados):
        print(f"  [{i}] Texto: '{texto}' | Confianza: {confianza:.2%}")
    
    # Buscar el número
    import re
    for bbox, texto, confianza in resultados:
        numeros = re.findall(r'\d+\.?\d*', texto)
        if numeros:
            print(f"✅ Número encontrado: {numeros[0]}")

except ImportError as e:
    print(f"❌ Error importando: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
