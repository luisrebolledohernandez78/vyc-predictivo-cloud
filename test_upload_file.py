#!/usr/bin/env python
"""
Script para probar la subida de archivo y análisis
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

django.setup()

from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO
from core.models import Activo, AnalisisTermico

# Crear una imagen de prueba simple
print("Creando imagen de prueba...")
img = Image.new('RGB', (400, 300), color='red')
img_io = BytesIO()
img.save(img_io, format='PNG')
img_io.seek(0)

archivo = SimpleUploadedFile(
    "test_thermal.png",
    img_io.getvalue(),
    content_type="image/png"
)

# Buscar un activo para prueba
try:
    activo = Activo.objects.first()
    if not activo:
        print("❌ No hay activos en la BD")
        sys.exit(1)
    
    print(f"✅ Usando activo: {activo.nombre} (ID: {activo.id})")
    
    # Intentar guardar el archivo
    print("Guardando archivo...")
    activo.foto_termica = archivo
    activo.save()
    
    print(f"✅ Archivo guardado")
    print(f"   Ruta: {activo.foto_termica}")
    print(f"   URL: {activo.foto_termica.url}")
    
    # Intentar crear análisis
    print("\nCreando análisis...")
    analisis, creado = AnalisisTermico.objects.update_or_create(
        activo=activo,
        defaults={
            'temperatura_promedio': 48.5,
            'temperatura_maxima': 55.0,
            'temperatura_minima': 35.0,
            'rango_minimo': 35.0,
            'rango_maximo': 55.0,
            'porcentaje_zona_critica': 0,
            'porcentaje_zona_alerta': 0,
            'porcentaje_zona_caliente': 0,
            'estado': 'bueno',
        }
    )
    
    print(f"✅ Análisis {'creado' if creado else 'actualizado'}")
    print(f"   ID: {analisis.id}")
    print(f"   Temperatura máxima: {analisis.temperatura_maxima}°C")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
