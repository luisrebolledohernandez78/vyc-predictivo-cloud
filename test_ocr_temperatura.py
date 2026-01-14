"""
Script de prueba para verificar que el OCR extrae temperaturas correctamente
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
django.setup()

from core.analisis_termico import AnalizadorTermico
from core.models import Activo

def test_ocr_en_activos():
    """Prueba OCR en todos los activos con fotos térmicas"""
    
    analizador = AnalizadorTermico()
    
    # Obtener activos que tengan foto térmica
    activos_con_foto = Activo.objects.filter(foto_termica__isnull=False).exclude(foto_termica='')
    
    print(f"\n📸 Probando OCR con {activos_con_foto.count()} imágenes FLIR...\n")
    
    for activo in activos_con_foto[:5]:  # Primeros 5 activos
        print(f"🔍 Analizando: {activo.nombre}")
        
        resultado = analizador.analizar_imagen(activo.foto_termica)
        
        print(f"   Resultado: {resultado}")
        print(f"   Temperatura máxima: {resultado.get('temperatura_maxima', 'N/A')}°C")
        print(f"   Estado: {resultado.get('estado', 'N/A')}")
        print(f"   Mensaje: {resultado.get('mensaje', 'N/A')}")
        print()

if __name__ == '__main__':
    test_ocr_en_activos()
