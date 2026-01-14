#!/usr/bin/env python
"""Test simple del OCR sin Django"""
import sys
sys.path.insert(0, 's:\\vyc-predictivo-cloud\\backend')

import logging
logging.basicConfig(level=logging.INFO, 
    format='%(message)s')

from core.analisis_termico import AnalizadorTermico
import glob
import os

# Buscar última imagen
pattern = 's:\\vyc-predictivo-cloud\\backend\\media\\termografias\\activos\\*.jpg'
archivos = sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)

if not archivos:
    print("No encontre imagenes")
    sys.exit(1)

print(f"\nUltima imagen: {os.path.basename(archivos[0])}\n")

# Analizar
analizador = AnalizadorTermico()
print("\nAnalizando...")
resultado = analizador.analizar_imagen(archivos[0])

print("\n" + "="*60)
print("RESULTADO")
print("="*60)
if 'error' in resultado:
    print(f"Error: {resultado['error']}")
else:
    print(f"Temperatura: {resultado['temperatura_maxima']}°C")
    print(f"Estado: {resultado['estado'].upper()}")
    print(f"Mensaje: {resultado['mensaje']}")
