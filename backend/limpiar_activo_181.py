#!/usr/bin/env python
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from core.models import Activo, AnalisisTermico, MuestreoActivo

print('═══════════════════════════════════════════════════════════════')
print('LIMPIEZA DE DATOS - ACTIVO 181 (Motor Cabezal 1)')
print('═══════════════════════════════════════════════════════════════')

activo = Activo.objects.get(id=181)

# Obtener y eliminar análisis térmicos
analisis_count = AnalisisTermico.objects.filter(activo_id=181).count()
print(f'\n🗑️  ELIMINANDO ANÁLISIS TÉRMICOS:')
print(f'   Total a eliminar: {analisis_count}')
AnalisisTermico.objects.filter(activo_id=181).delete()
print(f'   ✅ Eliminados {analisis_count} registros de AnalisisTermico')

# Obtener y eliminar muestreos
muestreo_count = MuestreoActivo.objects.filter(activo_id=181).count()
print(f'\n🗑️  ELIMINANDO MUESTREOS:')
print(f'   Total a eliminar: {muestreo_count}')
MuestreoActivo.objects.filter(activo_id=181).delete()
print(f'   ✅ Eliminados {muestreo_count} registros de MuestreoActivo')

# Resetear estado del activo
activo.estado = 'sin_medicion'
activo.foto_termica.delete() if activo.foto_termica else None
activo.save()
print(f'\n🔄 ESTADO DEL ACTIVO:')
print(f'   ✅ Estado resetado a: sin_medicion')
print(f'   ✅ Foto térmica eliminada')

print(f'\n═══════════════════════════════════════════════════════════════')
print(f'✅ LIMPIEZA COMPLETADA - LISTO PARA COMENZAR DESDE CERO')
print(f'═══════════════════════════════════════════════════════════════')
