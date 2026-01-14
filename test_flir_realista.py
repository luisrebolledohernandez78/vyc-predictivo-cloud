#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test del analizador térmico con imagen FLIR realista
"""
import os
import sys
import django
from pathlib import Path

# Cambiar al directorio correcto
os.chdir('s:\\vyc-predictivo-cloud')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, 's:\\vyc-predictivo-cloud\\backend')

django.setup()

from core.analisis_termico import AnalizadorTermico
from pathlib import Path

print("TEST: Analizador Termico - Imagen FLIR Realista")
print("=" * 60)

# Probar con imagen FLIR realista
imagen_path = Path('imagen_flir_realista.jpg')
if not imagen_path.exists():
    print(f"ERROR: No encontrada: {imagen_path}")
    sys.exit(1)

print(f"Analizando: {imagen_path}")
print(f"Tamaño: {imagen_path.stat().st_size} bytes")

analizador = AnalizadorTermico()
resultado = analizador.analizar_imagen(str(imagen_path))

print("\n" + "=" * 60)
if 'error' in resultado:
    print(f"ERROR: {resultado['error']}")
    sys.exit(1)

print("RESULTADOS:")
print("=" * 60)
print(f"Estado: {resultado['estado'].upper()}")
print(f"Mensaje: {resultado['mensaje']}")

print(f"\nTEMPERATURAS (simuladas 0-100C):")
print(f"   Promedio:  {resultado['temperatura_promedio']:.1f}C")
print(f"   Maxima:    {resultado['temperatura_maxima']:.1f}C")
print(f"   Minima:    {resultado['temperatura_minima']:.1f}C")

print(f"\nZONAS DETECTADAS:")
print(f"   Zona Critica (rojo):    {resultado['porcentaje_zona_critica']:.1f}%")
print(f"   Zona Alerta (naranja):  {resultado['porcentaje_zona_alerta']:.1f}%")
print(f"   Zona Caliente (total):  {resultado['porcentaje_zona_caliente']:.1f}%")

# Interpretar resultados
print(f"\nINTERPRETACION:")
if resultado['estado'] == 'critico':
    print(f"   [CRITICO] El motor tiene zonas muy calientes")
    print(f"   Accion: Revisar URGENTEMENTE - posible falla inminente")
elif resultado['estado'] == 'alerta':
    print(f"   [ALERTA] El motor esta operando con temperaturas elevadas")
    print(f"   Accion: Monitorear de cerca, posible mantenimiento preventivo")
else:
    print(f"   [NORMAL] Operacion dentro de parametros")

print("\nOK: Analisis completado exitosamente")
