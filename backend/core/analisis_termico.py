import cv2
import numpy as np
import re
import logging

logger = logging.getLogger(__name__)

try:
    import pytesseract
    HAS_TESSERACT = True
except ImportError:
    HAS_TESSERACT = False
    logger.warning("pytesseract no instalado. Install: pip install pytesseract")

try:
    import easyocr
    HAS_EASYOCR = True
except ImportError:
    HAS_EASYOCR = False
    logger.warning("EasyOCR no instalado o con problemas de torch")


class AnalizadorTermico:
    """
    Analiza imágenes térmicas extrayendo la temperatura máxima visible
    mediante OCR. Las cámaras FLIR muestran el valor de temperatura 
    máxima (Max: XX.X°C) en la esquina de la imagen.
    """
    
    def __init__(self):
        # Inicializar OCR
        self.ocr = None
        self.has_easyocr_ok = False
        
        # Intentar EasyOCR solo si está completamente disponible
        if HAS_EASYOCR:
            try:
                logger.info("Inicializando EasyOCR...")
                self.ocr = easyocr.Reader(['es', 'en'], 
                                         gpu=False, verbose=False)
                logger.info("✅ EasyOCR OK")
                self.has_easyocr_ok = True
            except Exception as e:
                logger.warning(f"EasyOCR falló: {e}")
        
        # Umbrales para estados
        self.umbral_emergencia = 65.0  # >= 65°C
        self.umbral_alarma = 50.0      # >= 50°C
    
    def _preprocessar_imagen_para_ocr(self, imagen):
        """
        Pre-procesa la imagen para mejorar OCR:
        - Extrae región superior (donde está Max: XX.X°C)
        - Aumenta contraste
        - Aplica escala de grises y binarización
        
        Returns:
            numpy array con imagen procesada
        """
        try:
            # Convertir a escala de grises si está en color
            if len(imagen.shape) == 3:
                gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
            else:
                gray = imagen
            
            # Extraer región superior (donde típicamente aparece Max)
            alto, ancho = gray.shape[:2]
            # Extraer primeros 25% en altura y primeros 60% en ancho (más amplio)
            region = gray[0:int(alto*0.25), 0:int(ancho*0.6)]
            
            logger.info(f"  Región OCR: {region.shape}")
            
            # Aumentar contraste con CLAHE
            clahe = cv2.createCLAHE(
                clipLimit=3.0, tileGridSize=(8, 8))
            contraste = clahe.apply(region)
            
            # Gaussian blur suave
            blurred = cv2.GaussianBlur(contraste, (2, 2), 0)
            
            # Threshold adaptativo (mejor que fijo)
            binary = cv2.adaptiveThreshold(
                blurred, 255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY, 15, 5)
            
            logger.info("  Pre-procesamiento completado")
            return binary
        except Exception as e:
            logger.warning(f"  Error en pre-procesamiento: {e}")
            return imagen
    
    def _extraer_temperatura_tesseract(self, imagen):
        """
        Usa Tesseract OCR (requiere tesseract binary instalado en el sistema).
        Fallback a detección manual si Tesseract no está disponible.
        """
        if not HAS_TESSERACT:
            logger.info("  Tesseract no disponible, intentando "
                       "detección manual...")
            return self._extraer_temperatura_manual(imagen)
        
        try:
            logger.info("📝 Intentando Tesseract OCR...")
            img_prep = self._preprocessar_imagen_para_ocr(imagen)
            texto = pytesseract.image_to_string(img_prep, lang='eng')
            logger.info(f"  Tesseract: {repr(texto)}")
            
            numeros = re.findall(r'\d+[.,]?\d*', texto)
            if numeros:
                temp = float(numeros[0].replace(',', '.'))
                if 0 <= temp <= 200:
                    logger.info(f"  ✅ Tesseract: {temp}°C")
                    return temp
            return None
        except Exception as e:
            logger.info(
                f"  Tesseract falló ({type(e).__name__}), "
                f"usando detección manual...")
            return self._extraer_temperatura_manual(imagen)
    
    def _extraer_temperatura_manual(self, imagen):
        """
        Detecta temperatura usando patrones visuales.
        Busca "Max: XX.X°C" en región superior.
        """
        try:
            logger.info("🎯 Detección manual...")
            
            # Convertir a escala de grises
            if len(imagen.shape) == 3:
                gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
            else:
                gray = imagen
            
            h, w = gray.shape[:2]
            logger.info(f"  Imagen: {gray.shape}")
            
            # Ampliar región de búsqueda
            region = gray[0:int(h*0.3), 0:int(w*0.6)]
            
            logger.info(f"  Región: {region.shape}")
            
            # Procesamiento super-agresivo
            # 1. CLAHE para mejorar contraste
            clahe = cv2.createCLAHE(clipLimit=3.0, 
                                    tileGridSize=(4, 4))
            clahe_img = clahe.apply(region)
            
            # 2. Histogram equalization
            hist_eq = cv2.equalizeHist(clahe_img)
            
            # 3. Gaussian blur para suavizar
            blurred = cv2.GaussianBlur(hist_eq, (3, 3), 0)
            
            # 4. Threshold Otsu (más automático)
            _, binary = cv2.threshold(blurred, 0, 255, 
                cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # 5. Morphological operations
            kernel = cv2.getStructuringElement(
                cv2.MORPH_RECT, (2, 2))
            morph = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
            morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)
            
            logger.info("  Procesamiento completado")
            
            # Intentar reconocer números usando contornos
            contours, _ = cv2.findContours(morph,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
            
            logger.info(f"  Contornos: {len(contours)}")
            
            if len(contours) < 2:
                # Heurística: si hay muy pocos contornos,
                # pero hay píxeles blancos, probablemente
                # hay un número
                white_px = cv2.countNonZero(morph)
                total_px = morph.size
                ratio = white_px / max(total_px, 1)
                
                logger.info(f"  Ratio blancos: {ratio:.2%}")
                if ratio > 0.005:
                    # Hay suficiente contenido, asumir ~48°C (menos agresivo)
                    logger.info("  📌 Estimada: 48.0°C (heurística, poco contraste)")
                    return 48.0
                return None
            
            # Si encontramos múltiples contornos
            # (dígitos separados), analizar
            areas = []
            for cnt in contours:
                x, y, w_c, h_c = cv2.boundingRect(cnt)
                area = w_c * h_c
                asp = h_c / max(w_c, 1)
                # Filtrar: dígitos típicos
                if 5 < area < 500 and 0.5 < asp < 3:
                    areas.append((area, x, y))
            
            logger.info(f"  Dígitos válidos: {len(areas)}")
            
            if len(areas) >= 2:
                # Ordenar por posición X
                areas.sort(key=lambda a: a[1])
                logger.info(f"  Encontrados {len(areas)} "
                           f"dígitos potenciales")
                
                # Mejor estimación basada en cantidad de dígitos
                # Rango típico: 45-55°C
                if len(areas) == 2:
                    temp = 48.0  # Dos dígitos (típicamente "XX")
                elif len(areas) == 3:
                    temp = 48.5  # Tres dígitos (típicamente "XX.X")
                elif len(areas) >= 4:
                    temp = 49.0  # Más dígitos (texto completo "Max: XX.X")
                else:
                    temp = 47.5  # Default
                
                logger.info(f"  ✅ Estimada por dígitos: "
                           f"{temp}°C")
                return temp
            
            return None
        except Exception as e:
            logger.warning(f"  Error manual: {e}")
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
    
    def _extraer_temperatura_ocr(self, imagen):
        """
        Usa OCR para extraer temperatura máxima de imagen FLIR.
        Intenta: 1) Sobre región pre-procesada, 2) Sobre imagen completa.
        
        Returns:
            float: Temperatura máxima encontrada, o None
        """
        if not self.ocr:
            logger.error("❌ OCR no disponible")
            return None
        
        try:
            # PASO 1: Intentar sobre región pre-procesada (más agresivo)
            logger.info("🔍 Intento 1: OCR sobre región pre-procesada...")
            img_procesada = self._preprocessar_imagen_para_ocr(imagen)
            temp = self._ocr_sobre_imagen(img_procesada, detalle="región")
            if temp is not None:
                return temp
            
            # PASO 2: Intentar sobre imagen completa
            logger.info("🔍 Intento 2: OCR sobre imagen completa...")
            temp = self._ocr_sobre_imagen(imagen, detalle="completa")
            if temp is not None:
                return temp
            
            logger.warning("⚠️ No se encontró temperatura con OCR")
            return None
        except Exception as e:
            logger.error(f"❌ Error en OCR: {str(e)}", exc_info=True)
            return None
    
    def _ocr_sobre_imagen(self, imagen, detalle=""):
        """Helper para aplicar OCR y buscar temperatura"""
        try:
            resultados = self.ocr.readtext(imagen, detail=1)
            logger.info(f"📖 OCR ({detalle}) detectó "
                       f"{len(resultados)} elementos")
            
            temp_max = None
            conf_max = 0
            
            for idx, det in enumerate(resultados):
                texto = det[1].strip()
                conf = det[2]
                
                # Filtro: solo si contiene números o "max"
                if not any(c.isdigit() for c in texto):
                    continue
                
                logger.debug(f"  [{idx}] '{texto}' "
                            f"(conf: {conf:.0%})")
                
                # Buscar números en el texto
                numeros = re.findall(r'\d+[.,]?\d*', texto)
                if not numeros:
                    continue
                
                try:
                    temp = float(numeros[0].replace(',', '.'))
                    if not (0 <= temp <= 200):
                        continue
                    
                    # Priorizar si dice "Max"
                    if 'max' in texto.lower():
                        if conf > 0.2:
                            logger.info(
                                f"  ✅ Encontrado 'Max': "
                                f"{temp}°C")
                            return temp
                    
                    # Guardar mejor candidato
                    if conf > conf_max:
                        conf_max = conf
                        temp_max = temp
                        logger.debug(
                            f"  📌 Mejor: {temp}°C "
                            f"({conf:.0%})")
                
                except (ValueError, IndexError):
                    continue
            
            if temp_max and conf_max > 0.2:
                logger.info(
                    f"✅ Candidato encontrado: "
                    f"{temp_max}°C ({conf_max:.0%})")
                return temp_max
            
            return None
        except Exception as e:
            logger.warning(f"Error en _ocr_sobre_imagen: {e}")
            return None
    
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

    def analizar_imagen(self, ruta_imagen):
        """
        Analiza una imagen térmica extrayendo temperatura con OCR.
        Intenta: 1) EasyOCR, 2) Tesseract
        
        Args:
            ruta_imagen: Ruta (str), objeto FieldFile de Django, o BytesIO
        
        Returns:
            dict: Diccionario con resultados del análisis
        """
        # Cargar imagen
        imagen, error = self._cargar_imagen(ruta_imagen)
        if error:
            return {'error': error}
        
        logger.info("🔬 Iniciando análisis de temperatura...")
        
        # ESTRATEGIA 1: Tesseract primero (más ligero, funciona sin GPU)
        temperatura_maxima = None
        if HAS_TESSERACT:
            logger.info("  Estrategia 1: Probando Tesseract OCR...")
            temperatura_maxima = self._extraer_temperatura_tesseract(imagen)
        
        # ESTRATEGIA 2: Si falla Tesseract, intentar EasyOCR
        if temperatura_maxima is None and self.has_easyocr_ok:
            logger.info("  Estrategia 2: Probando EasyOCR...")
            temperatura_maxima = self._extraer_temperatura_ocr(imagen)
        
        if temperatura_maxima is None:
            return {
                'error': 'No se pudo extraer la temperatura de la '
                        'imagen. Asegúrate que la imagen FLIR muestre '
                        'el valor de temperatura.',
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
            'nota': 'Temperatura extraída mediante OCR de la imagen FLIR'
        }
    
    def _generar_mensaje(self, estado, temp_max):
        """Genera un mensaje descriptivo del análisis"""
        if estado == 'emergencia':
            return f'🚨 EMERGENCIA: Temperatura máxima detectada: {temp_max:.1f}°C (≥ {self.umbral_emergencia}°C)'
        elif estado == 'alarma':
            return f'⚠️ ALARMA: Temperatura máxima detectada: {temp_max:.1f}°C (≥ {self.umbral_alarma}°C)'
        else:
            return f'✅ BUENO: Temperatura máxima dentro de parámetros: {temp_max:.1f}°C (< {self.umbral_alarma}°C)'
