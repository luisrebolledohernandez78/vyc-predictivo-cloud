from django.core.management.base import BaseCommand
from core.models import Sucursal, Area


class Command(BaseCommand):
    help = 'Crea automáticamente las 3 áreas predefinidas para todas las sucursales que no las tengan'

    def handle(self, *args, **options):
        areas_predefinidas = [
            ('aserradero', 'Aserradero'),
            ('elaborado', 'Elaborado'),
            ('caldera', 'Caldera'),
        ]
        
        total_sucursales = Sucursal.objects.count()
        sucursales_actualizadas = 0
        areas_creadas = 0
        
        self.stdout.write(self.style.SUCCESS(f'Procesando {total_sucursales} sucursales...'))
        
        for sucursal in Sucursal.objects.all():
            # Contar cuántas áreas tiene esta sucursal
            areas_existentes = sucursal.areas.count()
            
            if areas_existentes < 3:
                sucursales_actualizadas += 1
                self.stdout.write(f'  - {sucursal.nombre} ({sucursal.cliente.nombre}): {areas_existentes}/3 áreas')
                
                for area_nombre, area_label in areas_predefinidas:
                    area, created = Area.objects.get_or_create(
                        sucursal=sucursal,
                        nombre=area_nombre,
                        defaults={'descripcion': f'Área de {area_label}'}
                    )
                    if created:
                        areas_creadas += 1
                        self.stdout.write(f'    ✓ Creada: {area_label}')
                    else:
                        self.stdout.write(f'    - Ya existía: {area_label}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Completado:\n'
                f'   - Sucursales procesadas: {sucursales_actualizadas}\n'
                f'   - Áreas creadas: {areas_creadas}\n'
                f'   - Total áreas en sistema: {Area.objects.count()}'
            )
        )
