import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Cliente, Sucursal, Area, Equipo, Activo

print("="*80)
print("DATOS POBLADOS EN LA BASE DE DATOS")
print("="*80)

for cliente in Cliente.objects.all():
    print(f"\n📋 CLIENTE: {cliente.nombre}")
    print(f"   Email: {cliente.email}")
    
    sucursales = Sucursal.objects.filter(cliente=cliente)
    print(f"   Sucursales: {sucursales.count()}")
    
    for sucursal in sucursales:
        print(f"\n   └─ SUCURSAL: {sucursal.nombre}")
        
        areas = Area.objects.filter(sucursal=sucursal)
        for area in areas:
            equipos = Equipo.objects.filter(area=area)
            activos_totales = Activo.objects.filter(equipo__area=area).count()
            
            print(f"      ├─ ÁREA: {area.get_nombre_display()} ({equipos.count()} equipos, {activos_totales} activos)")
            
            for equipo in equipos[:3]:  # Mostrar primeros 3 equipos
                activos = Activo.objects.filter(equipo=equipo)
                print(f"      │  ├─ Equipo: {equipo.nombre} ({activos.count()} activos)")
                for activo in activos[:2]:  # Primeros 2 activos
                    print(f"      │  │  ├─ Activo: {activo.nombre}")
            
            if equipos.count() > 3:
                print(f"      │  └─ ... y {equipos.count() - 3} equipos más")

print("\n" + "="*80)
print("RESUMEN TOTAL")
print("="*80)
print(f"Total Clientes: {Cliente.objects.count()}")
print(f"Total Sucursales: {Sucursal.objects.count()}")
print(f"Total Áreas: {Area.objects.count()}")
print(f"Total Equipos: {Equipo.objects.count()}")
print(f"Total Activos: {Activo.objects.count()}")
print("="*80)
