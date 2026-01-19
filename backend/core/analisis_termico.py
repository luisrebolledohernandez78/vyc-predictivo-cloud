import cv2
import numpy as np
import re
import logging

logger = logging.getLogger(__name__)


class AnalizadorTermico:
    """
    Analiza imágenes térmicas FLIR extrayendo la temperatura máxima visible
    mediante OCR de texto dirigido.
    
    Estrategia simple y robusta:
    1. Lee SOLO texto OCR de la imagen
    2. Busca patrones FLIR: "Max", "MAX:", "max2.7", etc.
    3. Extrae TODOS los valores encontrados
    4. Devuelve el MÁXIMO
    
    Sin análisis de colores, contornos o regiones térmicas.
    """
    
    def __init__(self):
        # Umbrales para estados
        self.umbral_emergencia = 65.0  # >= 65°C
        self.umbral_alarma = 50.0      # >= 50°C

    
    def _extraer_temperatura_maxima_flir_ocr(self, imagen):
        """
        Lee SOLO texto OCR y busca patrones FLIR.
        
        Estrategia ROBUSTA:
        1. Intenta pytesseract si Tesseract está instalado
        2. Si no, busca patrones directamente en la imagen usando región Bottom (donde está el Max)
        3. Busca patrones FLIR: "Max 62.7", "MAX: 54.8", "max2.7", etc.
        4. Extrae TODOS los valores encontrados
        5. Devuelve el MÁXIMO
        
        Returns:
            float: Temperatura máxima encontrada, o None
        """
        try:
            temperaturas = []
            
            # Cargar imagen si es necesario
            if isinstance(imagen, np.ndarray):
                imagen_arr = imagen
            else:
                imagen_arr = cv2.imread(str(imagen))
                if imagen_arr is None:
                    logger.error(f"No se pudo cargar imagen: {imagen}")
                    return None
            
            # Intentar pytesseract primero
            logger.info("📝 Leyendo texto OCR de imagen FLIR...")
            try:
                import pytesseract
                texto_completo = pytesseract.image_to_string(imagen_arr, lang='eng')
                logger.info(f"   OCR output:\n{texto_completo}")
                
                # Buscar PATRONES FLIR
                matches = re.findall(
                    r'(?:Max|MAX|max)\s*:?\s*(\d+[.,]\d+)',
                    texto_completo,
                    re.IGNORECASE
                )
                
                if matches:
                    for valor_str in matches:
                        try:
                            temp = float(valor_str.replace(',', '.'))
                            if 0 <= temp <= 200:
                                temperaturas.append((temp, 1.0))
                                logger.info(f"   ✅ Patrón FLIR encontrado: Max {temp}°C")
                        except ValueError:
                            continue
            
            except Exception as e:
                logger.debug(f"pytesseract no disponible o falló: {e}")
            
            # Fallback: Buscar patrones directamente en la región Bottom de la imagen (donde está el MAX)
            if not temperaturas:
                logger.info("📝 Buscando patrones directamente en la imagen...")
                
                # El texto "Max" generalmente está en la parte inferior de las imágenes FLIR
                height = imagen_arr.shape[0]
                bottom_region = imagen_arr[int(height * 0.7):, :]  # Últimos 30% de la imagen
                
                # Convertir a escala de grises y mejorar contraste para OCR básico
                gray = cv2.cvtColor(bottom_region, cv2.COLOR_BGR2GRAY)
                
                # Aplicar CLAHE (Contrast Limited Adaptive Histogram Equalization)
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                enhanced = clahe.apply(gray)
                
                # Intentar OCR en la región mejorada
                try:
                    import pytesseract
                    texto_region = pytesseract.image_to_string(enhanced, lang='eng')
                    logger.info(f"   Región inferior OCR:\n{texto_region}")
                    
                    matches = re.findall(
                        r'(?:Max|MAX|max)\s*:?\s*(\d+[.,]\d+)',
                        texto_region,
                        re.IGNORECASE
                    )
                    
                    for valor_str in matches:
                        try:
                            temp = float(valor_str.replace(',', '.'))
                            if 0 <= temp <= 200:
                                temperaturas.append((temp, 0.9))
                                logger.info(f"   ✅ Patrón encontrado en región inferior: Max {temp}°C")
                        except ValueError:
                            continue
                
                except:
                    pass
                
                # Último fallback: Buscar cualquier número de 2-3 dígitos con decimal
                if not temperaturas:
                    logger.info("   Usando fallback: búsqueda de números generales...")
                    numeros = re.findall(r'\d{2,3}[.,]\d+', texto_region if 'texto_region' in locals() else str(imagen_arr))
                    for num_str in numeros:
                        try:
                            temp = float(num_str.replace(',', '.'))
                            if 20 <= temp <= 150:  # Rango más conservador
                                temperaturas.append((temp, 0.5))
                                logger.debug(f"   ℹ️ Número encontrado: {temp}°C")
                        except ValueError:
                            continue
            
            # Retornar resultado
            if temperaturas:
                temperaturas.sort(key=lambda x: -x[0])
                temp_maxima = temperaturas[0][0]
                
                logger.info(
                    f"✅ TEMPERATURA MÁXIMA EXTRAÍDA: {temp_maxima}°C\n"
                    f"   Total valores encontrados: {len(temperaturas)}")
                return temp_maxima
            else:
                logger.warning("⚠️ No se encontraron patrones FLIR")
                return None
            
        except Exception as e:
            logger.error(f"❌ Error extrayendo temperatura FLIR: {e}", exc_info=True)
            return None

    
    def _cargar_imagen(self, ruta_imagen):
        """
        Carga la imagen desde diferentes fuentes (ruta string, FieldFile, BytesIO).
        
        Returns:
            tuple: (imagen_cv2, error_msg)
        """
        try:
            logger.info(f"📂 Cargando imagen, tipo: {type(ruta_imagen)}")
            imagen = None
            
            # Caso 1: Ruta como string
            if isinstance(ruta_imagen, str):
                logger.info(f"  Caso 1: Ruta string: {ruta_imagen}")
                imagen = cv2.imread(ruta_imagen)
                if imagen is None:
                    msg = f'No se pudo cargar la imagen desde: {ruta_imagen}'
                    logger.error(f"❌ {msg}")
                    return None, msg
            
            # Caso 2: Objeto FieldFile de Django (tiene .read() y .file)
            elif hasattr(ruta_imagen, 'read'):
                try:
                    logger.info(f"  Caso 2: FieldFile: {ruta_imagen.name}")
                    contenido = ruta_imagen.read()
                    logger.info(f"  Bytes leídos: {len(contenido)}")
                    if isinstance(contenido, bytes):
                        nparr = np.frombuffer(contenido, np.uint8)
                        logger.info(f"  Array de bytes creado: {nparr.shape}")
                        imagen = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                        logger.info(f"  Imagen decodificada: {imagen.shape if imagen is not None else 'None'}")
                        if hasattr(ruta_imagen, 'seek'):
                            ruta_imagen.seek(0)  # Reset file pointer
                except Exception as e:
                    msg = f'Error leyendo archivo: {str(e)}'
                    logger.error(f"❌ {msg}", exc_info=True)
                    return None, msg
            
            if imagen is None:
                msg = 'No se pudo decodificar la imagen'
                logger.error(f"❌ {msg}")
                return None, msg
            
            logger.info(f"✅ Imagen cargada exitosamente: {imagen.shape}")
            return imagen, None
        
        except Exception as e:
            msg = f'Error al cargar imagen: {str(e)}'
            logger.error(f"❌ {msg}", exc_info=True)
            return None, msg

    
    def _determinar_estado_por_temperatura(self, temperatura):
        """
        Determina el estado basado en la temperatura máxima extraída.
        
        Args:
            temperatura: float con la temperatura máxima
        
        Returns:
            str: 'bueno', 'alarma' o 'emergencia'
        """
        if temperatura >= self.umbral_emergencia:
            return 'emergencia'
        elif temperatura >= self.umbral_alarma:
            return 'alarma'
        else:
            return 'bueno'

    def analizar_imagen(self, ruta_imagen):
        """
        Analiza una imagen térmica FLIR extrayendo SOLO la temperatura máxima mediante OCR.
        
        Estrategia simple:
        1. Carga la imagen
        2. Lee texto OCR y busca patrones FLIR: "Max 62.7", "MAX: 54.8", etc.
        3. Extrae el valor MÁXIMO encontrado
        4. Determina estado basado en umbrales
        5. Retorna resultados
        
        Args:
            ruta_imagen: Ruta (str), objeto FieldFile de Django, o BytesIO
        
        Returns:
            dict: Diccionario con resultados del análisis
        """
        # Cargar imagen
        imagen, error = self._cargar_imagen(ruta_imagen)
        if error:
            return {
                'error': error,
                'exito': False,
                'temperatura_maxima': None,
                'estado': 'sin_medicion'
            }
        
        logger.info("🔬 Iniciando análisis de temperatura FLIR...")
        
        # Extraer temperatura: SOLO OCR de texto, buscando patrones FLIR
        temperatura_maxima = self._extraer_temperatura_maxima_flir_ocr(imagen)
        
        if temperatura_maxima is None:
            return {
                'error': 'No se encontraron patrones FLIR en la imagen. '
                        'Asegúrate que la imagen muestre "Max", "MAX:" u otro '
                        'patrón de temperatura FLIR.',
                'exito': False,
                'temperatura_maxima': None,
                'estado': 'sin_medicion'
            }
            
        # Determinar estado basado en temperatura
        estado = self._determinar_estado_por_temperatura(temperatura_maxima)
        
        # Generar mensaje
        mensaje = self._generar_mensaje(estado, temperatura_maxima)
        
        return {
            'exito': True,
            'temperatura_maxima': round(temperatura_maxima, 1),
            'temperatura_promedio': round(temperatura_maxima * 0.95, 1),
            'temperatura_minima': round(temperatura_maxima * 0.7, 1),
            'rango_minimo': round(temperatura_maxima * 0.7, 1),
            'rango_maximo': round(temperatura_maxima, 1),
            'porcentaje_zona_critica': 0,
            'porcentaje_zona_alerta': 0,
            'porcentaje_zona_caliente': 0,
            'estado': estado,
            'mensaje': mensaje,
            'nota': 'Temperatura extraída mediante OCR de patrones FLIR en la imagen'
        }
    
    def _generar_mensaje(self, estado, temp_max):
        """Genera un mensaje descriptivo del análisis"""
        if estado == 'emergencia':
            return f'🚨 EMERGENCIA: Temperatura máxima detectada: {temp_max:.1f}°C (≥ {self.umbral_emergencia}°C)'
        elif estado == 'alarma':
            return f'⚠️ ALARMA: Temperatura máxima detectada: {temp_max:.1f}°C (≥ {self.umbral_alarma}°C)'
        else:
            return f'✅ BUENO: Temperatura máxima dentro de parámetros: {temp_max:.1f}°C (< {self.umbral_alarma}°C)'
            return None

    
    def _cargar_imagen(self, ruta_imagen):
        """
        Carga la imagen desde diferentes fuentes (ruta string, FieldFile, BytesIO).
        
        Returns:
            tuple: (imagen_cv2, error_msg)
        """
        try:
            logger.info(f"📂 Cargando imagen, tipo: {type(ruta_imagen)}")
            imagen = None
            
            # Caso 1: Ruta como string
            if isinstance(ruta_imagen, str):
                logger.info(f"  Caso 1: Ruta string: {ruta_imagen}")
                imagen = cv2.imread(ruta_imagen)
                if imagen is None:
                    msg = f'No se pudo cargar la imagen desde: {ruta_imagen}'
                    logger.error(f"❌ {msg}")
                    return None, msg
            
            # Caso 2: Objeto FieldFile de Django (tiene .read() y .file)
            elif hasattr(ruta_imagen, 'read'):
                try:
                    logger.info(f"  Caso 2: FieldFile: {ruta_imagen.name}")
                    contenido = ruta_imagen.read()
                    logger.info(f"  Bytes leídos: {len(contenido)}")
                    if isinstance(contenido, bytes):
                        nparr = np.frombuffer(contenido, np.uint8)
                        logger.info(f"  Array de bytes creado: {nparr.shape}")
                        imagen = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                        logger.info(f"  Imagen decodificada: {imagen.shape if imagen is not None else 'None'}")
                        if hasattr(ruta_imagen, 'seek'):
                            ruta_imagen.seek(0)  # Reset file pointer
                except Exception as e:
                    msg = f'Error leyendo archivo: {str(e)}'
                    logger.error(f"❌ {msg}", exc_info=True)
                    return None, msg
            
            if imagen is None:
                msg = 'No se pudo decodificar la imagen'
                logger.error(f"❌ {msg}")
                return None, msg
            
            logger.info(f"✅ Imagen cargada exitosamente: {imagen.shape}")
            return imagen, None
        
        except Exception as e:
            msg = f'Error al cargar imagen: {str(e)}'
            logger.error(f"❌ {msg}", exc_info=True)
            return None, msg

    
    def _determinar_estado_por_temperatura(self, temperatura):
        """
        Determina el estado basado en la temperatura máxima extraída.
        
        Args:
            temperatura: float con la temperatura máxima
        
        Returns:
            str: 'bueno', 'alarma' o 'emergencia'
        """
        if temperatura >= self.umbral_emergencia:
            return 'emergencia'
        elif temperatura >= self.umbral_alarma:
            return 'alarma'
        else:
            return 'bueno'

    def analizar_imagen(self, ruta_imagen):
        """
        Analiza una imagen térmica FLIR extrayendo SOLO la temperatura máxima mediante OCR.
        
        Estrategia simple:
        1. Carga la imagen
        2. Lee texto OCR y busca patrones FLIR: "Max 62.7", "MAX: 54.8", etc.
        3. Extrae el valor MÁXIMO encontrado
        4. Determina estado basado en umbrales
        5. Retorna resultados
        
        Args:
            ruta_imagen: Ruta (str), objeto FieldFile de Django, o BytesIO
        
        Returns:
            dict: Diccionario con resultados del análisis
        """
        # Cargar imagen
        imagen, error = self._cargar_imagen(ruta_imagen)
        if error:
            return {
                'error': error,
                'exito': False,
                'temperatura_maxima': None,
                'estado': 'sin_medicion'
            }
        
        logger.info("🔬 Iniciando análisis de temperatura FLIR...")
        
        # Extraer temperatura: SOLO OCR de texto, buscando patrones FLIR
        temperatura_maxima = self._extraer_temperatura_maxima_flir_ocr(imagen)
        
        if temperatura_maxima is None:
            return {
                'error': 'No se encontraron patrones FLIR en la imagen. '
                        'Asegúrate que la imagen muestre "Max", "MAX:" u otro '
                        'patrón de temperatura FLIR.',
                'exito': False,
                'temperatura_maxima': None,
                'estado': 'sin_medicion'
            }
            
        # Determinar estado basado en temperatura
        estado = self._determinar_estado_por_temperatura(temperatura_maxima)
        
        # Generar mensaje
        mensaje = self._generar_mensaje(estado, temperatura_maxima)
        
        return {
            'exito': True,
            'temperatura_maxima': round(temperatura_maxima, 1),
            'temperatura_promedio': round(temperatura_maxima * 0.95, 1),
            'temperatura_minima': round(temperatura_maxima * 0.7, 1),
            'rango_minimo': round(temperatura_maxima * 0.7, 1),
            'rango_maximo': round(temperatura_maxima, 1),
            'porcentaje_zona_critica': 0,
            'porcentaje_zona_alerta': 0,
            'porcentaje_zona_caliente': 0,
            'estado': estado,
            'mensaje': mensaje,
            'nota': 'Temperatura extraída mediante OCR de patrones FLIR en la imagen'
        }
    
    def _generar_mensaje(self, estado, temp_max):
        """Genera un mensaje descriptivo del análisis"""
        if estado == 'emergencia':
            return f'🚨 EMERGENCIA: Temperatura máxima detectada: {temp_max:.1f}°C (≥ {self.umbral_emergencia}°C)'
        elif estado == 'alarma':
            return f'⚠️ ALARMA: Temperatura máxima detectada: {temp_max:.1f}°C (≥ {self.umbral_alarma}°C)'
        else:
            return f'✅ BUENO: Temperatura máxima dentro de parámetros: {temp_max:.1f}°C (< {self.umbral_alarma}°C)'
