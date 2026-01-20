from django.core.management.base import BaseCommand
from django.utils import timezone
from random import choice, uniform
from datetime import date
from core.models import Activo, VibracionesAnalisis

class Command(BaseCommand):
    help = 'Pobla datos ficticios de vibraciones para todos los activos'

    def handle(self, *args, **options):
        # Resultados disponibles en VibracionesAnalisis - 5 estados para vibraciones
        RESULTADOS = ['bueno', 'observacion', 'alarma', 'falla', 'sin_medicion']
        
        # Obtener todos los activos
        activos = Activo.objects.filter(activo=True)
        
        if not activos.exists():
            self.stdout.write(self.style.WARNING('No hay activos para poblar'))
            return
        
        contador = 0
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
                fecha_muestreo=date.today(),
                observaciones=f'Datos ficticios para prueba - Resultado: {resultado}'
            )
            contador += 1
            self.stdout.write(
                f'✓ {activo.nombre} - RMS: {velocidad_rms} mm/s, Aceleración: {aceleracion} g, Resultado: {resultado}'
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Se poblaron {contador} registros de vibraciones')
        )
