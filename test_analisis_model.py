#!/usr/bin/env python
"""
Script para probar si el modelo AnalisisTermico tiene todos los campos necesarios
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

django.setup()

from core.models import AnalisisTermico, Activo

# Verificar que el modelo tiene todos los campos
print("✅ Campos del modelo AnalisisTermico:")
for field in AnalisisTermico._meta.fields:
    print(f"  - {field.name}: {field.get_internal_type()}")

# Campos requeridos por la vista
required_fields = [
    'temperatura_promedio',
    'temperatura_maxima',
    'temperatura_minima',
    'rango_minimo',
    'rango_maximo',
    'porcentaje_zona_critica',
    'porcentaje_zona_alerta',
    'porcentaje_zona_caliente',
    'estado'
]

print("\n✅ Verificando campos requeridos:")
field_names = [f.name for f in AnalisisTermico._meta.fields]
for field in required_fields:
    if field in field_names:
        print(f"  ✅ {field}")
    else:
        print(f"  ❌ FALTA: {field}")

print("\n✅ Test completado")
