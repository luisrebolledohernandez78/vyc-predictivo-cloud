#!/usr/bin/env python
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from core.models import Activo, AnalisisTermico, MuestreoActivo

print('═══════════════════════════════════════════════════════════════')
print('BÚSQUEDA DE ACTIVO CON ID=1')
print('═══════════════════════════════════════════════════════════════')

activo = Activo.objects.filter(id=1).first()
if activo:
    print(f'✅ ACTIVO ENCONTRADO:')
    print(f'  ID: {activo.id}')
    print(f'  Nombre: {activo.nombre}')
    print(f'  Equipo: {activo.equipo.nombre}')
    print(f'  Área: {activo.equipo.area.nombre}')
    print(f'  Estado: {activo.estado}')
    print(f'  Foto Térmica: {"Sí" if activo.foto_termica else "No"}')
    
    print(f'\n📊 ANÁLISIS TÉRMICOS:')
    analisis = AnalisisTermico.objects.filter(activo_id=1)
    if analisis.exists():
        print(f'  Total: {analisis.count()}')
        for i, a in enumerate(analisis.order_by('-creado'), 1):
            print(f'  [{i}] ID: {a.id}, Temp: {a.temperatura_promedio}°C, Máx: {a.temperatura_maxima}°C, Estado: {a.estado}, Creado: {a.creado}')
    else:
        print(f'  ❌ Sin análisis térmicos')
    
    print(f'\n📅 MUESTREOS:')
    muestreos = MuestreoActivo.objects.filter(activo_id=1)
    if muestreos.exists():
        print(f'  Total: {muestreos.count()}')
        for i, m in enumerate(muestreos.order_by('-fecha_muestreo'), 1):
            print(f'  [{i}] Fecha: {m.fecha_muestreo}')
    else:
        print(f'  ❌ Sin muestreos registrados')
else:
    print('❌ NO EXISTE ACTIVO CON ID=1')
    
    print(f'\n📋 ACTIVOS DISPONIBLES (primeros 20):')
    print('═══════════════════════════════════════════════════════════════')
    activos = Activo.objects.all()[:20]
    for a in activos:
        print(f'  ID: {a.id:3d} | Nombre: {a.nombre:30s} | Equipo: {a.equipo.nombre:20s} | Área: {a.equipo.area.nombre:15s}')
