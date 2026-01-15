#!/usr/bin/env python
"""
Script para probar la eliminación de foto térmica
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import User
from core.views import eliminar_foto_termica
from core.models import Activo, AnalisisTermico
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO

# Crear usuario de prueba
try:
    user = User.objects.create_user('test', 'test@test.com', 'test123')
except:
    user = User.objects.get(username='test')

# Buscar activo
activo = Activo.objects.first()
if not activo:
    print("❌ No hay activos en la BD")
    sys.exit(1)

print(f"✅ Usando activo: {activo.nombre} (ID: {activo.id})")

# Si no tiene foto, agregarla
if not activo.foto_termica:
    print("Agregando foto de prueba...")
    img = Image.new('RGB', (400, 300), color='red')
    img_io = BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)
    
    archivo = SimpleUploadedFile("test.png", img_io.getvalue(), content_type="image/png")
    activo.foto_termica = archivo
    activo.save()

# Si no hay análisis, agregarlo
if not AnalisisTermico.objects.filter(activo=activo).exists():
    print("Agregando análisis de prueba...")
    AnalisisTermico.objects.create(
        activo=activo,
        temperatura_promedio=48.5,
        temperatura_maxima=55.0,
        temperatura_minima=35.0,
        rango_minimo=35.0,
        rango_maximo=55.0,
        estado='bueno'
    )

print(f"Foto antes: {activo.foto_termica}")
print(f"Análisis antes: {AnalisisTermico.objects.filter(activo=activo).exists()}")
print(f"Estado antes: {activo.estado}")

# Crear request
factory = RequestFactory()
request = factory.post(f'/api/activo/{activo.id}/eliminar-foto-termica/')
request.user = user

print("\n🗑️  Eliminando foto térmica...")
try:
    response = eliminar_foto_termica(request, activo.id)
    
    import json
    data = json.loads(response.content)
    
    print(f"✅ Response status: {response.status_code}")
    print(f"✅ Response data: {data}")
    
    # Recargar activo
    activo.refresh_from_db()
    print(f"\nFoto después: {activo.foto_termica}")
    print(f"Análisis después: {AnalisisTermico.objects.filter(activo=activo).exists()}")
    print(f"Estado después: {activo.estado}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
