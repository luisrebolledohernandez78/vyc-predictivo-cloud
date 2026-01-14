"""
Script para crear una imagen térmica de prueba
Genera una imagen con gradiente de colores simulando una cámara térmica FLIR
"""
import cv2
import numpy as np
import os

def crear_imagen_termica_prueba(archivo_salida='imagen_termica_prueba.jpg'):
    """
    Crea una imagen térmica de prueba con zonas de diferentes temperaturas
    """
    # Crear imagen 400x300 en BGR (OpenCV usa BGR, no RGB)
    imagen = np.zeros((300, 400, 3), dtype=np.uint8)
    
    # Zona fría (azul) - lado izquierdo
    imagen[:100, :100] = [255, 100, 0]  # Azul
    
    # Zona templada (verde) - parte superior media
    imagen[:100, 100:250] = [0, 255, 0]  # Verde
    
    # Zona caliente (amarillo) - parte media
    imagen[100:200, 100:250] = [0, 255, 255]  # Amarillo
    
    # Zona MÁS caliente (naranja) - parte media-derecha
    imagen[100:200, 250:400] = [0, 165, 255]  # Naranja
    
    # Zona CRÍTICA (rojo intenso) - esquina derecha inferior
    imagen[200:300, 250:400] = [0, 0, 255]  # Rojo puro
    
    # Guardar imagen
    cv2.imwrite(archivo_salida, imagen)
    print(f"✅ Imagen térmica de prueba creada: {archivo_salida}")
    print(f"   Tamaño: 400x300 píxeles")
    print(f"   Zonas: Azul (frío) → Verde → Amarillo → Naranja → Rojo (caliente)")
    
    return archivo_salida

if __name__ == '__main__':
    crear_imagen_termica_prueba()
