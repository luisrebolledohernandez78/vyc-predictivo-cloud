"""
Script para probar el upload de imagen térmica
Simula un cliente HTTP subiendo una foto
"""
import requests
import json
from pathlib import Path

# Configuración
BASE_URL = 'http://127.0.0.1:8000'
LOGIN_URL = f'{BASE_URL}/login/'
UPLOAD_URL = f'{BASE_URL}/api/activo/1/subir-foto-termica/'

# Obtener la imagen de prueba
imagen_path = Path('imagen_termica_prueba.jpg')

if not imagen_path.exists():
    print("❌ No se encontró imagen_termica_prueba.jpg")
    print("   Ejecuta: python test_thermal_image.py")
    exit(1)

print(f"📁 Imagen encontrada: {imagen_path}")
print(f"📊 Tamaño: {imagen_path.stat().st_size} bytes")

# Crear sesión
session = requests.Session()

# Hacer login primero (necesario porque está @login_required)
print("\n🔐 Intentando login...")
login_data = {
    'username': 'admin',
    'password': 'admin'
}

try:
    response = session.post(LOGIN_URL, data=login_data, allow_redirects=True)
    print(f"   Status: {response.status_code}")
except Exception as e:
    print(f"   Error: {e}")

# Intentar subir imagen
print("\n📤 Subiendo imagen térmica...")
try:
    with open(imagen_path, 'rb') as f:
        files = {'foto': f}
        response = session.post(UPLOAD_URL)
    
    print(f"   Status: {response.status_code}")
    print(f"   Response:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
except Exception as e:
    print(f"   Error: {e}")
    print(f"   Posible causa: El servidor no está corriendo en {BASE_URL}")
    print(f"   O el activo_id=1 no existe")
