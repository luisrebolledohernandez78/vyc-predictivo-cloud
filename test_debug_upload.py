#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test upload contra endpoint de debug (sin autenticación)
"""
import os
import requests
from pathlib import Path

os.chdir('s:\\vyc-predictivo-cloud')

BASE_URL = 'http://127.0.0.1:8000'
IMAGEN = 'imagen_flir_realista.jpg'
ACTIVO_ID = 36  # Cambiar si es necesario

print("TEST: Upload a endpoint DEBUG (sin CSRF)")
print("=" * 60)

if not Path(IMAGEN).exists():
    print(f"ERROR: No encontrada: {IMAGEN}")
    exit(1)

print(f"Imagen: {IMAGEN}")
print(f"Tamaño: {Path(IMAGEN).stat().st_size} bytes")

# Intentar upload SIN login, SIN CSRF
print(f"\nIntentando upload a /api/debug/activo/{ACTIVO_ID}/test-upload/...")

with open(IMAGEN, 'rb') as f:
    files = {'foto': f}
    response = requests.post(
        f'{BASE_URL}/api/debug/activo/{ACTIVO_ID}/test-upload/',
        files=files
    )

print(f"Status: {response.status_code}")
print(f"Content-Type: {response.headers.get('content-type')}")
print(f"\nResponse:")
print(response.text)

if response.status_code == 200:
    print("\nOK: Upload exitoso")
else:
    print(f"\nERROR: {response.status_code}")
