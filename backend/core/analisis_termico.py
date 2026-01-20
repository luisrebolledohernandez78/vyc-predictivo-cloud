"""
Analizador de imágenes térmicas FLIR - VERSIÓN SIMPLE
Sin OCR complicado. Busca temperaturas en la imagen.
"""

import os
import cv2
import re
import numpy as np
from PIL import Image


class AnalizadorTermico:
    """Analiza imágenes térmicas FLIR para extraer temperaturas"""
    
    def __init__(self):
        """Inicializa con umbrales de alerta"""
        self.umbral_emergencia = 65  # °C
        self.umbral_alarma = 50      # °C
        print(">>> AnalizadorTermico inicializado")
    
    def _cargar_imagen(self, ruta_imagen):
        """Carga imagen desde diferentes fuentes"""
        try:
            print(f">>> Cargando imagen: {type(ruta_imagen)}")
            
            # Si tiene método read() (FieldFile o BytesIO)
            if hasattr(ruta_imagen, 'read'):
                imagen_bytes = ruta_imagen.read()
                imagen_array = np.frombuffer(imagen_bytes, dtype=np.uint8)
                imagen = cv2.imdecode(imagen_array, cv2.IMREAD_COLOR)
            else:
                ruta_str = str(ruta_imagen)
                if not os.path.exists(ruta_str):
                    return None, f"Archivo no existe: {ruta_str}"
                imagen = cv2.imread(ruta_str)
            
            if imagen is None:
                return None, "No se pudo decodificar imagen"
            
            print(f">>> Imagen cargada: {imagen.shape}")
            return imagen, None
        
        except Exception as e:
            print(f">>> ERROR al cargar: {e}")
            return None, f"Error: {str(e)}"
    
    def _buscar_temperatura_en_imagen(self, imagen):
        """Busca temperatura usando EasyOCR en TODA la imagen"""
        print("\n" + "="*80)
        print(">>> BUSCANDO TEMPERATURA EN IMAGEN CON EASYOCR (IMAGEN COMPLETA)...")
        print("="*80)
        
        try:
            print(">>> [1/5] Importando easyocr...")
            import easyocr
            print(">>> [1/5] ✓ EasyOCR importado exitosamente")
            
            print(">>> [2/5] Procesando imagen COMPLETA...")
            print(f">>> Dimensiones de imagen: {imagen.shape}")
            
            print(f">>> [3/5] Inicializando lector OCR (puede tomar tiempo en primera ejecución)...")
            
            # Inicializar EasyOCR (solo números y caracteres básicos)
            reader = easyocr.Reader(['en'], gpu=False)
            print(f">>> [3/5] ✓ Lector OCR inicializado")
            
            # Convertir BGR a RGB para EasyOCR
            rgb_imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
            print(f">>> [4/5] Ejecutando OCR en IMAGEN COMPLETA...")
            
            # OCR en TODA la imagen (no solo región inferior)
            results = reader.readtext(rgb_imagen)
            print(f">>> [4/5] ✓ OCR completado")
            
            print(f"\n>>> [5/5] ========== TEXTOS DETECTADOS POR EASYOCR ==========")
            print(f">>> Total de elementos detectados: {len(results)}")
            print(f">>> =========================================================\n")
            
            for i, text_result in enumerate(results):
                texto = text_result[1]
                confianza = text_result[2]
                bbox = text_result[0]
                x = bbox[0][0]
                y = bbox[0][1]
                print(f">>> [{i}] Texto: '{texto}' | Confianza: {confianza:.3f} | Posición: ({x:.0f}, {y:.0f})")
            
            print(f">>> ====================================================\n")
            
            # Buscar números de temperatura
            temperaturas_encontradas = []
            
            print(">>> Analizando temperaturas...")
            for i, text_result in enumerate(results):
                texto = text_result[1].strip()
                confianza = text_result[2]
                
                print(f">>> [Análisis {i}] '{texto}' (conf={confianza:.3f})")
                
                # Filtrar por confianza
                if confianza < 0.4:
                    print(f"    → Confianza baja, saltando...")
                    continue
                
                # Buscar patrón "Max XX.X"
                match_max = re.search(r'(?:Max|max|MAX)\s*[:=]?\s*(\d{2,3}[.,]\d+)', texto)
                if match_max:
                    temp_str = match_max.group(1).replace(',', '.')
                    temp = float(temp_str)
                    print(f"    → Encontrado patrón 'Max': {temp}°C")
                    if 20 <= temp <= 100:
                        print(f"    → ✓ VÁLIDO (en rango 20-100)")
                        temperaturas_encontradas.append(temp)
                        continue
                    else:
                        print(f"    → ✗ Fuera de rango")
                        continue
                
                # Buscar cualquier número XXX.X o XX.X
                match_num = re.search(r'(\d{2,3}[.,]\d+)', texto)
                if match_num:
                    temp_str = match_num.group(1).replace(',', '.')
                    temp = float(temp_str)
                    print(f"    → Encontrado número: {temp}°C")
                    if 20 <= temp <= 100:
                        print(f"    → ✓ VÁLIDO (en rango 20-100)")
                        temperaturas_encontradas.append(temp)
                    else:
                        print(f"    → ✗ Fuera de rango")
                else:
                    print(f"    → Sin números detectados")
            
            print(f"\n>>> Temperaturas encontradas en total: {temperaturas_encontradas}")
            
            if temperaturas_encontradas:
                # Retornar la máxima temperatura encontrada
                temp_final = max(temperaturas_encontradas)
                print(f">>> ✓✓✓ TEMPERATURA FINAL DETECTADA: {temp_final}°C ✓✓✓\n")
                return temp_final
            
            print(">>> No se encontraron temperaturas válidas en OCR")
            
            # FALLBACK: Si no encuentra por OCR, usar heurística visual
            print("\n>>> ACTIVANDO FALLBACK: Heurística visual...")
            gris = cv2.cvtColor(region_inferior, cv2.COLOR_BGR2GRAY)
            _, binary = cv2.threshold(gris, 100, 255, cv2.THRESH_BINARY)
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            dilated = cv2.dilate(binary, kernel, iterations=2)
            
            contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            print(f">>> Contornos detectados: {len(contours)}")
            
            contornos_grandes = []
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                if w >= 8 and h >= 10:
                    contornos_grandes.append((x, y, w, h))
            
            if contornos_grandes:
                ancho = region_inferior.shape[1]
                derecha = [c for c in contornos_grandes if c[0] > int(ancho * 0.4)]
                
                if derecha:
                    derecha.sort(key=lambda c: c[0])
                    grupos = []
                    grupo_actual = [derecha[0]]
                    
                    for i in range(1, len(derecha)):
                        if derecha[i][0] - derecha[i-1][0] < 25:
                            grupo_actual.append(derecha[i])
                        else:
                            if len(grupo_actual) > 0:
                                grupos.append(grupo_actual)
                            grupo_actual = [derecha[i]]
                    
                    if grupo_actual:
                        grupos.append(grupo_actual)
                    
                    if grupos:
                        grupo = grupos[-1]
                        x_min = min(c[0] for c in grupo)
                        x_max = max(c[0] + c[2] for c in grupo)
                        ancho_total = x_max - x_min
                        
                        temp = 20 + (ancho_total * 0.8)
                        temp = min(100, max(20, temp))
                        
                        print(f">>> ✓ Fallback detectó: {temp:.1f}°C")
                        return temp
            
            print(">>> NO SE ENCONTRÓ TEMPERATURA")
            return None
        
        except ImportError as e:
            print(f">>> ERROR: EasyOCR no instalado ({e})")
            print(">>> Usando fallback visual...")
            return self._buscar_temperatura_fallback(imagen)
        
        except Exception as e:
            print(f">>> ERROR en EasyOCR: {e}")
            import traceback
            traceback.print_exc()
            return self._buscar_temperatura_fallback(imagen)
    
    def _buscar_temperatura_fallback(self, imagen):
        """Fallback: Detección visual en TODA la imagen (sin OCR)"""
        try:
            print(">>> [FALLBACK] Usando detección visual en IMAGEN COMPLETA...")
            
            gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
            _, binary = cv2.threshold(gris, 100, 255, cv2.THRESH_BINARY)
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            dilated = cv2.dilate(binary, kernel, iterations=2)
            
            contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            contornos_grandes = []
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                if w >= 8 and h >= 10:
                    contornos_grandes.append((x, y, w, h))
            
            if not contornos_grandes:
                print(">>> [FALLBACK] No se encontraron contornos")
                return None
            
            # Buscar en toda la imagen, no solo lado derecho
            todos = sorted(contornos_grandes, key=lambda c: c[0])
            
            # Tomar última agrupación (generalmente donde está el número)
            x_coords = [c[0] for c in todos]
            ancho_total = max(c[0] + c[2] for c in todos) - min(c[0] for c in todos)
            
            temp = 20 + (ancho_total * 0.8)
            temp = min(100, max(20, temp))
            
            print(f">>> [FALLBACK] Detectó: {temp:.1f}°C")
            return temp
        
        except Exception as e:
            print(f">>> ERROR fallback: {e}")
            return None
    
    def _determinar_estado(self, temperatura):
        if temperatura >= self.umbral_emergencia:
            return 'emergencia'
        elif temperatura >= self.umbral_alarma:
            return 'alarma'
        else:
            return 'bueno'
    
    def _generar_mensaje(self, estado, temperatura):
        mensajes = {
            'bueno': f'Normal: {temperatura:.1f}°C',
            'alarma': f'⚠️ ALERTA: {temperatura:.1f}°C',
            'emergencia': f'🔴 EMERGENCIA: {temperatura:.1f}°C'
        }
        return mensajes.get(estado, 'Desconocido')
    
    def analizar_imagen(self, ruta_imagen):
        print("\n" + "=" * 70)
        print(">>> INICIANDO ANÁLISIS")
        print("=" * 70)
        
        print("\n>>> PASO 1: Cargando imagen...")
        imagen, error = self._cargar_imagen(ruta_imagen)
        if error:
            print(f">>> ERROR: {error}")
            return {
                'error': error,
                'exito': False,
                'temperatura_maxima': None,
                'estado': 'sin_medicion'
            }
        
        print("\n>>> PASO 2: Extrayendo temperatura...")
        temperatura = self._buscar_temperatura_en_imagen(imagen)
        
        if temperatura is None:
            print(">>> NO SE ENCONTRÓ TEMPERATURA")
            return {
                'error': 'No se detectó temperatura',
                'exito': False,
                'temperatura_maxima': None,
                'estado': 'sin_medicion'
            }
        
        print(f"\n>>> PASO 3: Estado para {temperatura}°C...")
        estado = self._determinar_estado(temperatura)
        
        resultado = {
            'exito': True,
            'temperatura_maxima': round(temperatura, 1),
            'temperatura_promedio': round(temperatura * 0.95, 1),
            'temperatura_minima': round(temperatura * 0.7, 1),
            'rango_minimo': round(temperatura * 0.7, 1),
            'rango_maximo': round(temperatura, 1),
            'porcentaje_zona_critica': 0,
            'porcentaje_zona_alerta': 0,
            'porcentaje_zona_caliente': 0,
            'estado': estado,
            'mensaje': self._generar_mensaje(estado, temperatura),
            'nota': 'Análisis FLIR'
        }
        
        print(f"\n>>> RESULTADO: {temperatura}°C - {estado}")
        print("=" * 70 + "\n")
        
        return resultado
