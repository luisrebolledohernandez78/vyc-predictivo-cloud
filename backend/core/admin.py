from django.contrib import admin
from .models import Cliente, Sucursal, Area


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'ciudad', 'activo', 'creado')
    list_filter = ('activo', 'creado', 'ciudad')
    search_fields = ('nombre', 'email', 'contacto_nombre')
    readonly_fields = ('creado', 'actualizado')
    
    fieldsets = (
        ('Información General', {
            'fields': ('nombre', 'descripcion', 'activo')
        }),
        ('Contacto', {
            'fields': ('email', 'telefono', 'direccion', 'ciudad', 'pais')
        }),
        ('Contacto Principal', {
            'fields': ('contacto_nombre', 'contacto_puesto', 'contacto_email', 'contacto_telefono')
        }),
        ('Información Empresa', {
            'fields': ('ruc_nit', 'industria', 'empleados')
        }),
        ('Auditoría', {
            'fields': ('creado', 'actualizado'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cliente', 'ciudad', 'activo', 'creado')
    list_filter = ('activo', 'creado', 'cliente', 'ciudad')
    search_fields = ('nombre', 'email', 'cliente__nombre')
    readonly_fields = ('creado', 'actualizado')
    
    fieldsets = (
        ('Información General', {
            'fields': ('cliente', 'nombre', 'descripcion', 'activo')
        }),
        ('Contacto', {
            'fields': ('email', 'telefono', 'direccion', 'ciudad', 'pais')
        }),
        ('Contacto Principal', {
            'fields': ('contacto_nombre', 'contacto_puesto', 'contacto_email', 'contacto_telefono')
        }),
        ('Auditoría', {
            'fields': ('creado', 'actualizado'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('get_nombre_display', 'sucursal', 'activo', 'creado')
    list_filter = ('activo', 'creado', 'nombre', 'sucursal__cliente')
    search_fields = ('nombre', 'sucursal__nombre', 'sucursal__cliente__nombre')
    readonly_fields = ('creado', 'actualizado')
    
    fieldsets = (
        ('Información General', {
            'fields': ('sucursal', 'nombre', 'descripcion', 'activo')
        }),
        ('Auditoría', {
            'fields': ('creado', 'actualizado'),
            'classes': ('collapse',)
        }),
    )

