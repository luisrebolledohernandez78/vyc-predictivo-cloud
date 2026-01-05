from django.db import models
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime


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

