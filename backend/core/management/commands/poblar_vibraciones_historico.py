from django.core.management.base import BaseCommand
from django.utils import timezone
from random import choice, uniform
from datetime import date, timedelta
from core.models import Activo, VibracionesAnalisis

class Command(BaseCommand):
    help = 'Pobla datos históricos de vibraciones para todos los activos (6 muestras por activo)'

    def handle(self, *args, **options):
        # Resultados disponibles en VibracionesAnalisis - 5 estados para vibraciones
        RESULTADOS = ['bueno', 'observacion', 'alarma', 'falla', 'sin_medicion']
        
        # Obtener todos los activos
        activos = list(Activo.objects.filter(activo=True))
        
        if not activos:
            self.stdout.write(self.style.WARNING('No hay activos para poblar'))
            return
        
        # Limpiar registros anteriores
        VibracionesAnalisis.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Registros anteriores eliminados\n'))
        
        contador_total = 0
        fecha_inicio = date.today() - timedelta(days=5)  # Comienza desde hace 5 días
        
        # Para cada circuito de análisis (6 días)
        for dia_offset in range(6):
            fecha_circuito = fecha_inicio + timedelta(days=dia_offset)
            self.stdout.write(f'📅 CIRCUITO {dia_offset + 1} - Fecha: {fecha_circuito.strftime("%d/%m/%Y")}')
            
            # Para cada activo en ese circuito
            for activo in activos:
                # Generar datos ficticios
                velocidad_rms = round(uniform(2.0, 10.0), 2)
                aceleracion = round(uniform(0.3, 2.5), 2)
                frecuencia_dominante = round(uniform(10.0, 500.0), 2)
                desplazamiento = round(uniform(1.0, 50.0), 2)
                resultado = choice(RESULTADOS)
                
                # Crear registro de análisis
                analisis = VibracionesAnalisis.objects.create(
                    activo=activo,
                    velocidad_rms=velocidad_rms,
                    aceleracion=aceleracion,
                    frecuencia_dominante=frecuencia_dominante,
                    desplazamiento=desplazamiento,
                    resultado=resultado,
                    fecha_muestreo=fecha_circuito,
                    observaciones=f'Circuito de análisis - {fecha_circuito.strftime("%d/%m/%Y")}'
                )
                contador_total += 1
                
                self.stdout.write(
                    f'  ✓ {activo.nombre}: RMS {velocidad_rms} mm/s | Aceleración {aceleracion} g | {resultado.upper()}'
                )
            
            self.stdout.write('')
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Se poblaron {contador_total} registros de vibraciones históricos')
        )
        self.stdout.write(
            self.style.SUCCESS(f'✅ Total: {len(activos)} activos × 6 circuitos = {len(activos) * 6} registros')
        )
