#!/usr/bin/env python
"""
Test del OCR mejorado para verificar que detecta temperaturas en imágenes FLIR
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from backend.core.analisis_termico import AnalizadorTermico
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Buscar últimas imágenes termales
import glob
pattern = 's:\\vyc-predictivo-cloud\\backend\\media\\termografias\\activos\\*.jpg'
archivos = sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)

if not archivos:
    logger.error("❌ No se encontraron imágenes termales")
    exit(1)

print(f"\n✅ Encontradas {len(archivos)} imágenes")
print(f"📸 Última imagen: {archivos[0]}\n")

# Test del analizador
analizador = AnalizadorTermico()
resultado = analizador.analizar_imagen(archivos[0])

print("\n" + "="*60)
print("RESULTADO DEL ANÁLISIS")
print("="*60)
import json
print(json.dumps(resultado, indent=2, ensure_ascii=False))
