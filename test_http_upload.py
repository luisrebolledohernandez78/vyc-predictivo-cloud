"""
Test simular upload a través de requests HTTP
Verifica qué error retorna específicamente el servidor
"""
import requests
import json
from pathlib import Path
import re

BASE_URL = 'http://127.0.0.1:8000'
IMAGEN_PATH = 'imagen_termica_prueba.jpg'

print("🧪 Test de Upload de Imagen Térmica")
print("=" * 60)

# Verificar que la imagen existe
if not Path(IMAGEN_PATH).exists():
    print(f"❌ No se encontró: {IMAGEN_PATH}")
    exit(1)

print(f"✅ Imagen encontrada: {IMAGEN_PATH}")

# Crear sesión para mantener cookies
session = requests.Session()

print("\n🔐 Haciendo GET a login para obtener CSRF token...")
resp_login_get = session.get(f'{BASE_URL}/login/')
print(f"   Status: {resp_login_get.status_code}")

# Extraer CSRF token del HTML
csrf_token = None
if 'csrfmiddlewaretoken' in resp_login_get.text:
    match = re.search(r'<input[^>]*name="csrfmiddlewaretoken"[^>]*value="([^"]*)"', resp_login_get.text)
    if match:
        csrf_token = match.group(1)
        print(f"   ✅ CSRF token obtenido: {csrf_token[:20]}...")

print("\n🔑 Haciendo POST al login...")
resp_login = session.post(
    f'{BASE_URL}/login/',
    data={
        'username': 'admin',
        'password': 'admin',
        'csrfmiddlewaretoken': csrf_token
    },
    allow_redirects=True
)
print(f"   Status: {resp_login.status_code}")

# Obtener nuevo CSRF token después del login
print("\n🔗 Obteniendo nuevo CSRF token post-login...")
resp_activos = session.get(f'{BASE_URL}/activos/')
if 'csrfmiddlewaretoken' in resp_activos.text:
    match = re.search(r'<input[^>]*name="csrfmiddlewaretoken"[^>]*value="([^"]*)"', resp_activos.text)
    if match:
        csrf_token = match.group(1)
        print(f"   ✅ Nuevo CSRF token: {csrf_token[:20]}...")

# Intentar subir con activo_id=1
print("\n📤 Subiendo imagen a activo_id=1...")
with open(IMAGEN_PATH, 'rb') as f:
    files = {'foto': f}
    data = {'csrfmiddlewaretoken': csrf_token}
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': 'application/json'
    }
    resp = session.post(
        f'{BASE_URL}/api/activo/1/subir-foto-termica/',
        files=files,
        data=data,
        headers=headers
    )

print(f"   Status: {resp.status_code}")
print(f"   Content-Type: {resp.headers.get('content-type')}")
print(f"\n   Response body:")

try:
    data = resp.json()
    print(json.dumps(data, indent=3, ensure_ascii=False))
    
    if data.get('success'):
        print("\n✅ Upload exitoso!")
        if 'analisis' in data:
            print("\n📊 Análisis recibido:")
            print(json.dumps(data['analisis'], indent=3, ensure_ascii=False))
    else:
        print(f"\n❌ Error: {data.get('error', 'Unknown error')}")
except Exception as e:
    print(f"   {resp.text[:500]}")
    print(f"\n❌ Error al parsear JSON: {e}")
