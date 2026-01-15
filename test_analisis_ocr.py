#!/usr/bin/env python
"""
Script para probar el análisis de imagen térmica
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

django.setup()

from PIL import Image
from io import BytesIO
from core.analisis_termico import AnalizadorTermico
from core.models import Activo

# Buscar activo con foto térmica
activo_con_foto = None
for activo in Activo.objects.filter(foto_termica__isnull=False):
    if activo.foto_termica:
        activo_con_foto = activo
        break

if not activo_con_foto:
    print("❌ No hay activos con foto térmica")
    # Crear uno de prueba
    print("Creando imagen de prueba...")
    img = Image.new('RGB', (400, 300), color='red')
    img.text_anchor = "la"
    
    # Agregar texto a la imagen
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), "Max: 55.5C", fill="white")
    
    img_io = BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)
    
    from django.core.files.uploadedfile import SimpleUploadedFile
    archivo = SimpleUploadedFile("test.png", img_io.getvalue(), content_type="image/png")
    
    activo = Activo.objects.first()
    if activo:
        activo.foto_termica = archivo
        activo.save()
        activo_con_foto = activo
        print(f"✅ Imagen de prueba creada para {activo.nombre}")

if activo_con_foto:
    print(f"\n🔬 Analizando foto de: {activo_con_foto.nombre}")
    print(f"   Ruta: {activo_con_foto.foto_termica}")
    
    try:
        analizador = AnalizadorTermico()
        resultado = analizador.analizar_imagen(activo_con_foto.foto_termica)
        
        print("\n✅ Resultado del análisis:")
        for key, value in resultado.items():
            print(f"   {key}: {value}")
            
    except Exception as e:
        print(f"❌ Error en análisis: {e}")
        import traceback
        traceback.print_exc()
