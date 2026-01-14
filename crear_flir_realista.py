"""
Crear imagen térmica similar a FLIR real
Basada en la foto que el usuario mostró
"""
import cv2
import numpy as np

def crear_imagen_flir_realista():
    """
    Crea imagen térmica similar a FLIR real
    Colores reales: Magenta/Púrpura (frío) → Amarillo → Naranja → Rojo (caliente)
    """
    # Crear imagen 400x500
    imagen = np.zeros((500, 400, 3), dtype=np.uint8)
    
    # Fondo magenta/púrpura (zonas más frías - baja temp)
    imagen[:, :] = [128, 0, 128]  # Magenta base
    
    # Zonas gradualmente más calientes
    # Parte superior: púrpura más oscura
    imagen[0:80, :] = [100, 10, 100]  # Púrpura oscuro
    
    # Parte media-superior: magenta más claro
    imagen[80:150, :] = [150, 20, 150]  # Magenta claro
    
    # Parte media: naranja oscuro
    imagen[150:250, :] = [0, 165, 255]  # Naranja (BGR)
    
    # Parte media-inferior: naranja más intenso
    imagen[250:350, :] = [0, 200, 255]  # Naranja intenso
    
    # Parte inferior: rojo intenso (zona más caliente)
    imagen[350:500, :] = [0, 0, 255]  # Rojo puro
    
    # Agregar gradiente para hacerlo más realista (simulate heat distribution)
    for y in range(imagen.shape[0]):
        for x in range(imagen.shape[1]):
            # Gradiente horizontal para simular geometría del motor
            intensity = int((x / imagen.shape[1]) * 50)
            if y < 80:
                imagen[y, x] = [min(255, 100 + intensity), 10, min(255, 100 + intensity)]
            elif y < 150:
                imagen[y, x] = [min(255, 150 + intensity), 20, min(255, 150 + intensity)]
            elif y < 250:
                imagen[y, x] = [min(255, intensity), min(255, 165 + intensity), min(255, 255)]
            elif y < 350:
                imagen[y, x] = [min(255, intensity), min(255, 200 + intensity), min(255, 255)]
            else:
                imagen[y, x] = [min(255, intensity), min(255, intensity), 255]
    
    # Guardar imagen
    cv2.imwrite('imagen_flir_realista.jpg', imagen)
    print("✅ Imagen FLIR realista creada: imagen_flir_realista.jpg")
    print("   Dimensiones: 400x500")
    print("   Colores: Magenta (frío) → Naranja → Rojo (caliente)")
    
    return 'imagen_flir_realista.jpg'

if __name__ == '__main__':
    crear_imagen_flir_realista()
