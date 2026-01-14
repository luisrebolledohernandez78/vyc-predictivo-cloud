from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime


class UserProfile(models.Model):
    """Modelo para extender el perfil del usuario"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    
    # Timestamps
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Perfil de {self.user.username}"


# Signal para crear automáticamente el perfil cuando se crea un usuario
@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    """Crea automáticamente el perfil cuando se crea un nuevo usuario"""
    if created:
        UserProfile.objects.get_or_create(user=instance)


class Cliente(models.Model):
    """Modelo para clientes/empresas"""
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=300, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    pais = models.CharField(max_length=100, blank=True)
    
    # Información de contacto
    contacto_nombre = models.CharField(max_length=200, blank=True)
    contacto_puesto = models.CharField(max_length=100, blank=True)
    contacto_email = models.EmailField(blank=True)
    contacto_telefono = models.CharField(max_length=20, blank=True)
    
    # Información de la empresa
    ruc_nit = models.CharField(max_length=50, blank=True, unique=True)
    industria = models.CharField(max_length=100, blank=True)
    empleados = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1)])
    
    # Timestamps
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    
    # Estado
    activo = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-creado']
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
    
    def __str__(self):
        return self.nombre


class Sucursal(models.Model):
    """Modelo para sucursales/ubicaciones de clientes"""
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='sucursales')
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=300, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    pais = models.CharField(max_length=100, blank=True)
    
    # Información de contacto
    contacto_nombre = models.CharField(max_length=200, blank=True)
    contacto_puesto = models.CharField(max_length=100, blank=True)
    contacto_email = models.EmailField(blank=True)
    contacto_telefono = models.CharField(max_length=20, blank=True)
    
    # Timestamps
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    
    # Estado
    activo = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-creado']
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursales'
        unique_together = ('cliente', 'nombre')
    
    def __str__(self):
        return f"{self.nombre} - {self.cliente.nombre}"


class Area(models.Model):
    """Modelo para áreas dentro de una sucursal"""
    AREA_CHOICES = [
        ('aserradero', 'Aserradero'),
        ('elaborado', 'Elaborado'),
        ('caldera', 'Caldera'),
    ]
    
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='areas')
    nombre = models.CharField(max_length=100, choices=AREA_CHOICES)
    descripcion = models.TextField(blank=True, null=True)
    
    # Timestamps
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    
    # Estado
    activo = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['nombre']
        verbose_name = 'Área'
        verbose_name_plural = 'Áreas'
        unique_together = ('sucursal', 'nombre')
    
    def __str__(self):
        return f"{self.get_nombre_display()} - {self.sucursal.nombre}"


# Signal para crear automáticamente las 3 áreas cuando se crea una sucursal
@receiver(post_save, sender=Sucursal)
def crear_areas_sucursal(sender, instance, created, **kwargs):
    """Crea automáticamente las 3 áreas predefinidas cuando se crea una nueva sucursal"""
    if created:
        areas_predefinidas = [
            ('aserradero', 'Aserradero'),
            ('elaborado', 'Elaborado'),
            ('caldera', 'Caldera'),
        ]
        
        for area_nombre, area_label in areas_predefinidas:
            Area.objects.get_or_create(
                sucursal=instance,
                nombre=area_nombre,
                defaults={'descripcion': f'Área de {area_label}'}
            )


class Equipo(models.Model):
    """Modelo para equipos/máquinas dentro de un área"""
    
    # Estados del equipo
    ESTADO_CHOICES = [
        ('bueno', 'Bueno'),
        ('observacion', 'Observación'),
        ('alarma', 'Alarma'),
        ('falla', 'Falla'),
        ('sin_medicion', 'Sin Medición'),
    ]
    
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='equipos')
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    observaciones = models.CharField(max_length=500, default='Sin Observaciones', blank=True, null=True, help_text='Potencia, RPM, Voltaje, etc. (máx 500 caracteres)')
    
    # Estado
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='sin_medicion',
        help_text='Estado actual del equipo basado en mediciones'
    )
    
    # Timestamps
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    
    # Estado de actividad
    activo = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-creado']
        verbose_name = 'Equipo'
        verbose_name_plural = 'Equipos'
        unique_together = ('area', 'nombre')
    
    def __str__(self):
        return f"{self.nombre} - {self.area.get_nombre_display()}"


class Activo(models.Model):
    """Modelo para activos/componentes dentro de un equipo"""
    
    # Estados del activo
    ESTADO_CHOICES = [
        ('bueno', 'Bueno'),
        ('observacion', 'Observación'),
        ('alarma', 'Alarma'),
        ('emergencia', 'Emergencia'),
        ('falla', 'Falla'),
        ('sin_medicion', 'Sin Medición'),
    ]
    
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='activos')
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    observaciones = models.CharField(max_length=500, default='Sin Observaciones', blank=True, null=True, help_text='Potencia, RPM, Voltaje, Fases, etc. (máx 500 caracteres)')
    
    # Foto térmica (solo para activos en termografías)
    foto_termica = models.ImageField(upload_to='termografias/activos/', blank=True, null=True, help_text='Foto térmica del activo')
    
    # Estado
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='sin_medicion',
        help_text='Estado actual del activo basado en mediciones'
    )
    
    # Timestamps
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    
    # Estado de actividad
    activo = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-creado']
        verbose_name = 'Activo'
        verbose_name_plural = 'Activos'
    
    def __str__(self):
        return f"{self.nombre} - {self.equipo.nombre}"


class AnalisisTermico(models.Model):
    """Modelo para guardar análisis de imágenes térmicas"""
    
    activo = models.OneToOneField(Activo, on_delete=models.CASCADE, related_name='analisis_termico', null=True, blank=True)
    
    # Estadísticas térmicas
    temperatura_promedio = models.FloatField(default=0, help_text='Temperatura promedio estimada (0-100)')
    temperatura_minima = models.FloatField(default=0, help_text='Temperatura mínima detectada')
    temperatura_maxima = models.FloatField(default=0, help_text='Temperatura máxima detectada')
    porcentaje_zona_critica = models.FloatField(default=0, help_text='Porcentaje de píxeles en zona crítica')
    porcentaje_zona_alerta = models.FloatField(default=0, help_text='Porcentaje de píxeles en zona de alerta')
    
    # Rangos de temperatura operacional por zona - BUENO
    zona_bueno_min = models.FloatField(default=20, help_text='Temperatura mínima - Zona BUENO')
    zona_bueno_max = models.FloatField(default=50, help_text='Temperatura máxima - Zona BUENO')
    
    # Rangos de temperatura operacional por zona - ALARMA
    zona_alarma_min = models.FloatField(default=50, help_text='Temperatura mínima - Zona ALARMA')
    zona_alarma_max = models.FloatField(default=65, help_text='Temperatura máxima - Zona ALARMA')
    
    # Rangos de temperatura operacional por zona - EMERGENCIA
    zona_emergencia_min = models.FloatField(default=65, help_text='Temperatura mínima - Zona EMERGENCIA')
    zona_emergencia_max = models.FloatField(default=100, help_text='Temperatura máxima - Zona EMERGENCIA')
    
    # Rangos antiguos (compatibilidad)
    rango_minimo = models.FloatField(default=0, help_text='Rango mínimo de temperatura en °C')
    rango_maximo = models.FloatField(default=0, help_text='Rango máximo de temperatura en °C')
    
    # Estado del análisis
    ESTADO_CHOICES = [
        ('bueno', 'Bueno'),
        ('alarma', 'Alarma'),
        ('emergencia', 'Emergencia'),
        ('sin_medicion', 'Sin Medición'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='sin_medicion')
    
    # Metadata
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Análisis Térmico'
        verbose_name_plural = 'Análisis Térmicos'
    
    def __str__(self):
        return f"Análisis - {self.activo.nombre if self.activo else 'N/A'}"
