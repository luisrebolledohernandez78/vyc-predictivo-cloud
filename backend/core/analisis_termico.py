"""
Analizador de imágenes térmicas usando OpenCV
Detecta rangos de temperatura basados en colores HSV
"""

import cv2
import numpy as np
from PIL import Image
import io


class AnalizadorTermico:
    """
    Analiza imágenes térmicas para detectar zonas calientes.
    Las cámaras FLIR generan imágenes donde:
    - Rojo/Naranja = Zonas MÁS CALIENTES
    - Amarillo = Zonas CALIENTES
    - Verde = Zonas TEMPLADAS
    - Azul/Morado = Zonas FRÍAS
    """
    
    def __init__(self):
        # Rangos HSV para detección térmica (valores aproximados)
        # Rango crítico: Rojo muy intenso (temperatura muy alta)
        self.rango_critico_bajo = np.array([0, 100, 100])
        self.rango_critico_alto = np.array([10, 255, 255])
        
        # Rango de alerta: Naranja/Rojo (temperatura alta)
        self.rango_alerta_bajo = np.array([10, 80, 100])
        self.rango_alerta_alto = np.array([25, 255, 255])
        
        # Rango normal: Amarillo/Verde (temperatura normal)
        self.rango_normal_bajo = np.array([25, 50, 100])
        self.rango_normal_alto = np.array([90, 255, 255])
    
    def analizar_imagen(self, ruta_imagen):
        """
        Analiza una imagen térmica y devuelve estadísticas.
        
        Args:
            ruta_imagen: Ruta (str), objeto FieldFile de Django, o BytesIO
        
        Returns:
            dict: Diccionario con resultados del análisis
        """
        try:
            imagen = None
            
            # Caso 1: Ruta como string
            if isinstance(ruta_imagen, str):
                imagen = cv2.imread(ruta_imagen)
                if imagen is None:
                    return {'error': f'No se pudo cargar la imagen desde: {ruta_imagen}'}
            
            # Caso 2: Objeto FieldFile de Django (tiene .read() y .file)
            elif hasattr(ruta_imagen, 'read'):
                try:
                    contenido = ruta_imagen.read()
                    if isinstance(contenido, bytes):
                        nparr = np.frombuffer(contenido, np.uint8)
                        imagen = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                        if hasattr(ruta_imagen, 'seek'):
                            ruta_imagen.seek(0)  # Reset file pointer
                except Exception as e:
                    return {'error': f'Error leyendo archivo: {str(e)}'}
            
            if imagen is None:
                return {'error': 'No se pudo decodificar la imagen'}
            
            # Convertir BGR a HSV
            hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
            
            # Convertir BGR a HSV
            hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
            
            # Obtener total de píxeles
            total_pixeles = imagen.shape[0] * imagen.shape[1]
            
            # Detectar zonas críticas (rojo muy intenso)
            mascara_critica = cv2.inRange(hsv, self.rango_critico_bajo, self.rango_critico_alto)
            pixeles_criticos = np.count_nonzero(mascara_critica)
            
            # Detectar zonas de alerta (naranja/rojo)
            mascara_alerta = cv2.inRange(hsv, self.rango_alerta_bajo, self.rango_alerta_alto)
            pixeles_alerta = np.count_nonzero(mascara_alerta)
            
            # Detectar zonas normales (amarillo/verde)
            mascara_normal = cv2.inRange(hsv, self.rango_normal_bajo, self.rango_normal_alto)
            pixeles_normales = np.count_nonzero(mascara_normal)
            
            # Calcular porcentajes
            porcentaje_critico = (pixeles_criticos / total_pixeles) * 100
            porcentaje_alerta = (pixeles_alerta / total_pixeles) * 100
            porcentaje_normal = (pixeles_normales / total_pixeles) * 100
            
            # Zona combinada crítica+alerta
            mascara_combinada = cv2.bitwise_or(mascara_critica, mascara_alerta)
            pixeles_combinados = np.count_nonzero(mascara_combinada)
            porcentaje_zona_caliente = (pixeles_combinados / total_pixeles) * 100
            
            # Estimar temperatura promedio (mapear HSV a rango de temperatura)
            # Simplificación: usar V (Value) como proxy de temperatura
            v_promedio = np.mean(hsv[:, :, 2])
            temperatura_promedio = (v_promedio / 255) * 100  # 0-100°C
            
            # Encontrar punto más caliente (máximo V)
            temperatura_maxima = (np.max(hsv[:, :, 2]) / 255) * 100
            temperatura_minima = (np.min(hsv[:, :, 2]) / 255) * 100
            
            # Determinar estado
            if porcentaje_critico > 5:
                estado = 'critico'
            elif porcentaje_zona_caliente > 20:
                estado = 'alerta'
            else:
                estado = 'normal'
            
            return {
                'exito': True,
                'temperatura_promedio': round(temperatura_promedio, 2),
                'temperatura_maxima': round(temperatura_maxima, 2),
                'temperatura_minima': round(temperatura_minima, 2),
                'porcentaje_zona_critica': round(porcentaje_critico, 2),
                'porcentaje_zona_alerta': round(porcentaje_alerta, 2),
                'porcentaje_zona_caliente': round(porcentaje_zona_caliente, 2),
                'estado': estado,
                'mensaje': self._generar_mensaje(estado, porcentaje_zona_caliente, temperatura_maxima)
            }
        
        except Exception as e:
            return {'error': f'Error al analizar imagen: {str(e)}'}
    
    def _generar_mensaje(self, estado, porcentaje_caliente, temp_max):
        """Genera un mensaje descriptivo del análisis"""
        if estado == 'critico':
            return f'⚠️ CRÍTICO: {porcentaje_caliente:.1f}% de zona caliente detectada. Temp máx: {temp_max:.1f}°C'
        elif estado == 'alerta':
            return f'⚠️ ALERTA: {porcentaje_caliente:.1f}% de zona caliente detectada. Temp máx: {temp_max:.1f}°C'
        else:
            return f'✅ NORMAL: Operación dentro de parámetros normales'
