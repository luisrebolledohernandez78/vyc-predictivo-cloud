#!/usr/bin/env python
"""
Script para simular una subida de foto térmica (sin Flask/Django server)
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

django.setup()

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from core.views import subir_foto_termica
from core.models import Activo

# Crear usuario de prueba
try:
    user = User.objects.create_user('test', 'test@test.com', 'test123')
except:
    user = User.objects.get(username='test')

# Crear una imagen de prueba
img = Image.new('RGB', (400, 300), color='red')
img_io = BytesIO()
img.save(img_io, format='PNG')
img_io.seek(0)

archivo = SimpleUploadedFile(
    "test_thermal.png",
    img_io.getvalue(),
    content_type="image/png"
)

# Buscar o crear un activo
activo = Activo.objects.first()
if not activo:
    print("❌ No hay activos en la BD")
    sys.exit(1)

print(f"✅ Usando activo: {activo.nombre} (ID: {activo.id})")

# Crear request
factory = RequestFactory()
request = factory.post(f'/api/activo/{activo.id}/subir-foto-termica/', {'foto': archivo})
request.user = user

print("\n📤 Simulando subida de foto...")
try:
    response = subir_foto_termica(request, activo.id)
    
    import json
    data = json.loads(response.content)
    
    print(f"✅ Response status: {response.status_code}")
    print(f"✅ Response data:")
    for key, value in data.items():
        if isinstance(value, dict):
            print(f"   {key}:")
            for k, v in value.items():
                print(f"      {k}: {v}")
        else:
            print(f"   {key}: {value}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
