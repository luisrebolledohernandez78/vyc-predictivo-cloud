from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import models
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Cliente, Sucursal, Area, Equipo, Activo, MuestreoActivo, TermografiaAnalisis, VibracionesAnalisis
from .forms import ClienteForm, SucursalForm, AreaForm, EquipoForm, ActivoForm, ExcelUploadForm
from .excel_parser import ExcelEquiposParser
import tempfile
import json
import csv
from decimal import Decimal
from django.http import HttpResponse


# Orden estándar de áreas
AREA_ORDER = {
    'aserradero': 1,
    'elaborado': 2,
    'caldera': 3,
}

def ordenar_areas(areas):
    """Ordena las áreas según el orden estándar: Aserradero, Elaborado, Caldera"""
    return sorted(areas, key=lambda a: AREA_ORDER.get(a.nombre, 999))


def welcome(request):
    """Página de bienvenida y login del portal"""
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/dashboard/')
        else:
            return redirect('/?error=1')
    
    return render(request, 'core/index.html')


@require_http_methods(["GET", "POST"])
def user_login(request):
    """Vista de login"""
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/dashboard/')
        else:
            return redirect('/login/?error=1')
    
    return render(request, 'core/login.html')


@require_http_methods(["GET"])
def user_logout(request):
    """Vista de logout"""
    logout(request)
    return redirect('/')


@login_required(login_url='login')
def dashboard(request):
    """Dashboard del usuario autenticado"""
    return render(request, 'core/dashboard_home.html', {
        'user': request.user
    })


# VIBRACIONES
@login_required(login_url='login')
def vibraciones(request):
    """Página de análisis de vibraciones"""
    clientes = Cliente.objects.filter(activo=True)
    context = {
        'user': request.user,
        'clientes': clientes,
        'modulo': 'vibraciones',
        'titulo': 'Análisis de Vibraciones',
        'descripcion': 'Monitorea y analiza las vibraciones de la maquinaria en tiempo real'
    }
    return render(request, 'core/vibraciones.html', context)


@login_required(login_url='login')
def crear_cliente_vibraciones(request):
    """Crear cliente desde módulo de vibraciones"""
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vibraciones')
    else:
        form = ClienteForm()
    
    context = {
        'form': form,
        'modulo': 'vibraciones',
        'titulo': 'Nuevo Cliente - Análisis de Vibraciones'
    }
    return render(request, 'core/cliente_form.html', context)


@login_required(login_url='login')
def editar_cliente_vibraciones(request, cliente_id):
    """Editar cliente desde módulo de vibraciones"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('vibraciones')
    else:
        form = ClienteForm(instance=cliente)
    
    context = {
        'form': form,
        'cliente': cliente,
        'modulo': 'vibraciones',
        'titulo': f'Editar {cliente.nombre}'
    }
    return render(request, 'core/cliente_form.html', context)


@login_required(login_url='login')
def eliminar_cliente_vibraciones(request, cliente_id):
    """Eliminar cliente desde módulo de vibraciones"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    cliente.delete()
    return redirect('vibraciones')


# TERMOGRAFÍAS
@login_required(login_url='login')
def termografias(request):
    """Página de termografía infrarroja"""
    clientes = Cliente.objects.filter(activo=True)
    context = {
        'user': request.user,
        'clientes': clientes,
        'modulo': 'termografias',
        'titulo': 'Termografía Infrarroja',
        'descripcion': 'Detecta anomalías térmicas en el equipamiento industrial'
    }
    return render(request, 'core/termografias.html', context)


@login_required(login_url='login')
def crear_cliente_termografias(request):
    """Crear cliente desde módulo de termografías"""
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('termografias')
    else:
        form = ClienteForm()
    
    context = {
        'form': form,
        'modulo': 'termografias',
        'titulo': 'Nuevo Cliente - Termografía'
    }
    return render(request, 'core/cliente_form.html', context)


@login_required(login_url='login')
def editar_cliente_termografias(request, cliente_id):
    """Editar cliente desde módulo de termografías"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('termografias')
    else:
        form = ClienteForm(instance=cliente)
    
    context = {
        'form': form,
        'cliente': cliente,
        'modulo': 'termografias',
        'titulo': f'Editar {cliente.nombre}'
    }
    return render(request, 'core/cliente_form.html', context)


@login_required(login_url='login')
def eliminar_cliente_termografias(request, cliente_id):
    """Eliminar cliente desde módulo de termografías"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    cliente.delete()
    return redirect('termografias')


# SUCURSALES - VIBRACIONES
@login_required(login_url='login')
def sucursales_vibraciones(request, cliente_id):
    """Página de sucursales para vibraciones"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursales = cliente.sucursales.filter(activo=True).order_by('nombre')
    context = {
        'user': request.user,
        'cliente': cliente,
        'sucursales': sucursales,
        'modulo': 'vibraciones',
        'titulo': f'Sucursales - {cliente.nombre}',
        'descripcion': 'Gestiona las sucursales y ubicaciones de tu cliente'
    }
    return render(request, 'core/sucursales.html', context)


@login_required(login_url='login')
def crear_sucursal_vibraciones(request, cliente_id):
    """Crear sucursal desde módulo de vibraciones"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    if request.method == 'POST':
        form = SucursalForm(request.POST)
        if form.is_valid():
            sucursal = form.save(commit=False)
            sucursal.cliente = cliente
            sucursal.save()
            return redirect('sucursales_vibraciones', cliente_id=cliente_id)
    else:
        form = SucursalForm()
    
    context = {
        'form': form,
        'cliente': cliente,
        'modulo': 'vibraciones',
        'titulo': f'Nueva Sucursal - {cliente.nombre}'
    }
    return render(request, 'core/sucursal_form.html', context)


@login_required(login_url='login')
def editar_sucursal_vibraciones(request, cliente_id, sucursal_id):
    """Editar sucursal desde módulo de vibraciones"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    
    if request.method == 'POST':
        form = SucursalForm(request.POST, request.FILES, instance=sucursal)
        if form.is_valid():
            form.save()
            return redirect('sucursales_vibraciones', cliente_id=cliente_id)
    else:
        form = SucursalForm(instance=sucursal)
    
    context = {
        'form': form,
        'cliente': cliente,
        'sucursal': sucursal,
        'modulo': 'vibraciones',
        'titulo': f'Editar {sucursal.nombre}'
    }
    return render(request, 'core/sucursal_form.html', context)


@login_required(login_url='login')
def eliminar_sucursal_vibraciones(request, cliente_id, sucursal_id):
    """Eliminar sucursal desde módulo de vibraciones"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    sucursal.delete()
    return redirect('sucursales_vibraciones', cliente_id=cliente_id)


# SUCURSALES - TERMOGRAFÍAS
@login_required(login_url='login')
def sucursales_termografias(request, cliente_id):
    """Página de sucursales para termografías"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursales = cliente.sucursales.filter(activo=True).order_by('nombre')
    context = {
        'user': request.user,
        'cliente': cliente,
        'sucursales': sucursales,
        'modulo': 'termografias',
        'titulo': f'Sucursales - {cliente.nombre}',
        'descripcion': 'Gestiona las sucursales y ubicaciones de tu cliente'
    }
    return render(request, 'core/sucursales.html', context)


@login_required(login_url='login')
def crear_sucursal_termografias(request, cliente_id):
    """Crear sucursal desde módulo de termografías"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    if request.method == 'POST':
        form = SucursalForm(request.POST)
        if form.is_valid():
            sucursal = form.save(commit=False)
            sucursal.cliente = cliente
            sucursal.save()
            return redirect('sucursales_termografias', cliente_id=cliente_id)
    else:
        form = SucursalForm()
    
    context = {
        'form': form,
        'cliente': cliente,
        'modulo': 'termografias',
        'titulo': f'Nueva Sucursal - {cliente.nombre}'
    }
    return render(request, 'core/sucursal_form.html', context)


@login_required(login_url='login')
def editar_sucursal_termografias(request, cliente_id, sucursal_id):
    """Editar sucursal desde módulo de termografías"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    
    if request.method == 'POST':
        form = SucursalForm(request.POST, request.FILES, instance=sucursal)
        if form.is_valid():
            form.save()
            return redirect('sucursales_termografias', cliente_id=cliente_id)
    else:
        form = SucursalForm(instance=sucursal)
    
    context = {
        'form': form,
        'cliente': cliente,
        'sucursal': sucursal,
        'modulo': 'termografias',
        'titulo': f'Editar {sucursal.nombre}'
    }
    return render(request, 'core/sucursal_form.html', context)


@login_required(login_url='login')
def eliminar_sucursal_termografias(request, cliente_id, sucursal_id):
    """Eliminar sucursal desde módulo de termografías"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    sucursal.delete()
    return redirect('sucursales_termografias', cliente_id=cliente_id)


# ÁREAS - VIBRACIONES
@login_required(login_url='login')
def areas_vibraciones(request, cliente_id, sucursal_id):
    """Página de áreas para vibraciones"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    areas = sucursal.areas.filter(activo=True)
    areas = ordenar_areas(areas)
    context = {
        'user': request.user,
        'cliente': cliente,
        'sucursal': sucursal,
        'areas': areas,
        'modulo': 'vibraciones',
        'titulo': f'Áreas - {sucursal.nombre}',
        'descripcion': 'Gestiona las áreas de monitoreo en esta sucursal'
    }
    return render(request, 'core/areas.html', context)


@login_required(login_url='login')
def equipos_totales_vibraciones(request, cliente_id, sucursal_id):
    """Página de TODOS los equipos de una sucursal (sin filtro de área)"""
    from django.db.models import Case, When
    
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    
    # Obtener todos los equipos de la sucursal (a través de áreas)
    # Ordenar por el orden definido en AREA_CHOICES: aserradero, elaborado, caldera
    equipos = Equipo.objects.filter(
        area__sucursal=sucursal,
        activo=True
    ).select_related(
        'area'
    ).annotate(
        area_orden=Case(
            When(area__nombre='aserradero', then=0),
            When(area__nombre='elaborado', then=1),
            When(area__nombre='caldera', then=2),
            default=3,
            output_field=models.IntegerField()
        )
    ).order_by('area_orden', 'nombre')
    
    # Calcular estadísticas
    areas = Area.objects.filter(sucursal=sucursal).distinct().count()
    equipos_count = equipos.count()
    activos_count = Activo.objects.filter(equipo__area__sucursal=sucursal, activo=True).count()
    
    context = {
        'user': request.user,
        'cliente': cliente,
        'sucursal': sucursal,
        'equipos': equipos,
        'modulo': 'vibraciones',
        'titulo': f'Todos los Equipos - {sucursal.nombre}',
        'descripcion': 'Listado total de todos los equipos monitoreados en esta planta',
        'es_listado_total': True,  # Bandera para indicar que es un listado total
        'total_areas': areas,
        'total_equipos': equipos_count,
        'total_activos': activos_count
    }
    return render(request, 'core/vibraciones/equipos_totales.html', context)


@login_required(login_url='login')
def editar_area_vibraciones(request, cliente_id, sucursal_id, area_id):
    """Editar área desde módulo de vibraciones"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    area = get_object_or_404(Area, id=area_id, sucursal=sucursal)
    
    if request.method == 'POST':
        form = AreaForm(request.POST, instance=area)
        if form.is_valid():
            form.save()
            return redirect('areas_vibraciones', cliente_id=cliente_id, sucursal_id=sucursal_id)
    else:
        form = AreaForm(instance=area)
    
    context = {
        'form': form,
        'cliente': cliente,
        'sucursal': sucursal,
        'area': area,
        'modulo': 'vibraciones',
        'titulo': f'Editar {area.get_nombre_display()}'
    }
    return render(request, 'core/area_form.html', context)


@login_required(login_url='login')
def eliminar_area_vibraciones(request, cliente_id, sucursal_id, area_id):
    """Eliminar área desde módulo de vibraciones"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    area = get_object_or_404(Area, id=area_id, sucursal=sucursal)
    area.delete()
    return redirect('areas_vibraciones', cliente_id=cliente_id, sucursal_id=sucursal_id)


# ÁREAS - TERMOGRAFÍAS
@login_required(login_url='login')
def areas_termografias(request, cliente_id, sucursal_id):
    """Página de áreas para termografías"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    areas = sucursal.areas.filter(activo=True)
    areas = ordenar_areas(areas)
    context = {
        'user': request.user,
        'cliente': cliente,
        'sucursal': sucursal,
        'areas': areas,
        'modulo': 'termografias',
        'titulo': f'Áreas - {sucursal.nombre}',
        'descripcion': 'Gestiona las áreas de monitoreo en esta sucursal'
    }
    return render(request, 'core/areas.html', context)


@login_required(login_url='login')
def activos_totales_termografias(request, cliente_id, sucursal_id):
    """Página de TODOS los activos de una sucursal (sin filtro de área)"""
    from django.db.models import Case, When
    
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    
    # Obtener todos los activos de la sucursal (a través de equipos)
    # Ordenar por el orden definido en AREA_CHOICES: aserradero, elaborado, caldera
    activos = Activo.objects.filter(
        equipo__area__sucursal=sucursal,
        activo=True
    ).select_related(
        'equipo',
        'equipo__area'
    ).annotate(
        area_orden=Case(
            When(equipo__area__nombre='aserradero', then=0),
            When(equipo__area__nombre='elaborado', then=1),
            When(equipo__area__nombre='caldera', then=2),
            default=3,
            output_field=models.IntegerField()
        )
    ).order_by('area_orden', 'equipo__nombre', 'nombre')
    
    # Calcular estadísticas
    areas = Area.objects.filter(sucursal=sucursal).distinct().count()
    equipos = Equipo.objects.filter(area__sucursal=sucursal).distinct().count()
    activos_count = activos.count()
    
    context = {
        'user': request.user,
        'cliente': cliente,
        'sucursal': sucursal,
        'activos': activos,
        'modulo': 'termografias',
        'titulo': f'Todos los Activos - {sucursal.nombre}',
        'descripcion': 'Listado total de todos los activos monitorados en esta planta',
        'es_listado_total': True,  # Bandera para indicar que es un listado total
        'total_areas': areas,
        'total_equipos': equipos,
        'total_activos': activos_count
    }
    return render(request, 'core/termografias/activos_totales.html', context)


@login_required(login_url='login')
def editar_area_termografias(request, cliente_id, sucursal_id, area_id):
    """Editar área desde módulo de termografías"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    area = get_object_or_404(Area, id=area_id, sucursal=sucursal)
    
    if request.method == 'POST':
        form = AreaForm(request.POST, instance=area)
        if form.is_valid():
            form.save()
            return redirect('areas_termografias', cliente_id=cliente_id, sucursal_id=sucursal_id)
    else:
        form = AreaForm(instance=area)
    
    context = {
        'form': form,
        'cliente': cliente,
        'sucursal': sucursal,
        'area': area,
        'modulo': 'termografias',
        'titulo': f'Editar {area.get_nombre_display()}'
    }
    return render(request, 'core/area_form.html', context)


@login_required(login_url='login')
def eliminar_area_termografias(request, cliente_id, sucursal_id, area_id):
    """Eliminar área desde módulo de termografías"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    area = get_object_or_404(Area, id=area_id, sucursal=sucursal)
    area.delete()
    return redirect('areas_termografias', cliente_id=cliente_id, sucursal_id=sucursal_id)


@api_view(["GET"])
def health(request):
    return Response({"status": "ok", "service": "vyc-predictivo-cloud"})


# EQUIPOS - VIBRACIONES
@login_required(login_url='login')
def equipos_vibraciones(request, cliente_id, sucursal_id, area_id):
    """Página de equipos para una área en vibraciones"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    area = get_object_or_404(Area, id=area_id, sucursal=sucursal)
    equipos = area.equipos.filter(activo=True).order_by('nombre')
    
    context = {
        'user': request.user,
        'cliente': cliente,
        'sucursal': sucursal,
        'area': area,
        'equipos': equipos,
        'modulo': 'vibraciones',
        'titulo': f'Equipos - {area.get_nombre_display()}',
        'descripcion': 'Gestiona los equipos y máquinas del área'
    }
    return render(request, 'core/vibraciones/equipos_totales.html', context)


@login_required(login_url='login')
def crear_equipo_vibraciones(request, cliente_id, sucursal_id, area_id):
    """Crear equipo desde módulo de vibraciones"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    area = get_object_or_404(Area, id=area_id, sucursal=sucursal)
    
    if request.method == 'POST':
        form = EquipoForm(request.POST)
        if form.is_valid():
            equipo = form.save(commit=False)
            equipo.area = area
            equipo.save()
            return redirect('equipos_vibraciones', cliente_id=cliente_id, sucursal_id=sucursal_id, area_id=area_id)
    else:
        form = EquipoForm()
    
    context = {
        'form': form,
        'cliente': cliente,
        'sucursal': sucursal,
        'area': area,
        'modulo': 'vibraciones',
        'titulo': f'Nuevo Equipo - {area.get_nombre_display()}'
    }
    return render(request, 'core/equipo_form.html', context)


@login_required(login_url='login')
def editar_equipo_vibraciones(request, cliente_id, sucursal_id, area_id, equipo_id):
    """Editar equipo desde módulo de vibraciones"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    area = get_object_or_404(Area, id=area_id, sucursal=sucursal)
    equipo = get_object_or_404(Equipo, id=equipo_id, area=area)
    
    if request.method == 'POST':
        form = EquipoForm(request.POST, instance=equipo)
        if form.is_valid():
            form.save()
            return redirect('equipos_vibraciones', cliente_id=cliente_id, sucursal_id=sucursal_id, area_id=area_id)
    else:
        form = EquipoForm(instance=equipo)
    
    context = {
        'form': form,
        'cliente': cliente,
        'sucursal': sucursal,
        'area': area,
        'equipo': equipo,
        'modulo': 'vibraciones',
        'titulo': f'Editar {equipo.nombre}'
    }
    return render(request, 'core/equipo_form.html', context)


@login_required(login_url='login')
def eliminar_equipo_vibraciones(request, cliente_id, sucursal_id, area_id, equipo_id):
    """Eliminar equipo desde módulo de vibraciones"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    area = get_object_or_404(Area, id=area_id, sucursal=sucursal)
    equipo = get_object_or_404(Equipo, id=equipo_id, area=area)
    equipo.delete()
    return redirect('equipos_vibraciones', cliente_id=cliente_id, sucursal_id=sucursal_id, area_id=area_id)


# ACTIVOS - VIBRACIONES
@login_required(login_url='login')
def activos_vibraciones(request, cliente_id, sucursal_id, area_id, equipo_id):
    """Página de activos para un equipo en vibraciones"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    area = get_object_or_404(Area, id=area_id, sucursal=sucursal)
    equipo = get_object_or_404(Equipo, id=equipo_id, area=area)
    activos = equipo.activos.filter(activo=True).order_by('nombre')
    
    context = {
        'user': request.user,
        'cliente': cliente,
        'sucursal': sucursal,
        'area': area,
        'equipo': equipo,
        'activos': activos,
        'modulo': 'vibraciones',
        'titulo': f'Activos - {equipo.nombre}',
        'descripcion': 'Gestiona los componentes y motores del equipo'
    }
    return render(request, 'core/vibraciones/activos_totales.html', context)


@login_required(login_url='login')
def crear_activo_vibraciones(request, cliente_id, sucursal_id, area_id, equipo_id):
    """Crear activo desde módulo de vibraciones"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    area = get_object_or_404(Area, id=area_id, sucursal=sucursal)
    equipo = get_object_or_404(Equipo, id=equipo_id, area=area)
    
    if request.method == 'POST':
        form = ActivoForm(request.POST)
        if form.is_valid():
            activo = form.save(commit=False)
            activo.equipo = equipo
            activo.save()
            return redirect('activos_vibraciones', cliente_id=cliente_id, sucursal_id=sucursal_id, area_id=area_id, equipo_id=equipo_id)
    else:
        form = ActivoForm()
    
    context = {
        'form': form,
        'cliente': cliente,
        'sucursal': sucursal,
        'area': area,
        'equipo': equipo,
        'modulo': 'vibraciones',
        'titulo': f'Nuevo Activo - {equipo.nombre}'
    }
    return render(request, 'core/activo_form.html', context)


@login_required(login_url='login')
def editar_activo_vibraciones(request, cliente_id, sucursal_id, area_id, equipo_id, activo_id):
    """Editar activo desde módulo de vibraciones"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    area = get_object_or_404(Area, id=area_id, sucursal=sucursal)
    equipo = get_object_or_404(Equipo, id=equipo_id, area=area)
    activo = get_object_or_404(Activo, id=activo_id, equipo=equipo)
    
    # Verificar si viene del listado total
    es_listado_total = request.GET.get('listado_total') == '1'
    
    if request.method == 'POST':
        form = ActivoForm(request.POST, instance=activo)
        if form.is_valid():
            form.save()
            # Redirigir al listado total si viene de allí, sino a activos por área
            if es_listado_total:
                return redirect('equipos_totales_vibraciones', cliente_id=cliente_id, sucursal_id=sucursal_id)
            else:
                return redirect('activos_vibraciones', cliente_id=cliente_id, sucursal_id=sucursal_id, area_id=area_id, equipo_id=equipo_id)
    else:
        form = ActivoForm(instance=activo)
    
    context = {
        'form': form,
        'cliente': cliente,
        'sucursal': sucursal,
        'area': area,
        'equipo': equipo,
        'activo': activo,
        'modulo': 'vibraciones',
        'titulo': f'Editar {activo.nombre}',
        'es_listado_total': es_listado_total
    }
    return render(request, 'core/activo_form.html', context)


@login_required(login_url='login')
def eliminar_activo_vibraciones(request, cliente_id, sucursal_id, area_id, equipo_id, activo_id):
    """Eliminar activo desde módulo de vibraciones"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    area = get_object_or_404(Area, id=area_id, sucursal=sucursal)
    equipo = get_object_or_404(Equipo, id=equipo_id, area=area)
    activo = get_object_or_404(Activo, id=activo_id, equipo=equipo)
    
    # Verificar si viene del listado total
    es_listado_total = request.GET.get('listado_total') == '1'
    
    activo.delete()
    
    # Redirigir al listado total si viene de allí, sino a activos por área
    if es_listado_total:
        return redirect('equipos_totales_vibraciones', cliente_id=cliente_id, sucursal_id=sucursal_id)
    else:
        return redirect('activos_vibraciones', cliente_id=cliente_id, sucursal_id=sucursal_id, area_id=area_id, equipo_id=equipo_id)


# UPLOAD EXCEL - VIBRACIONES
@login_required(login_url='login')
def upload_equipos_vibraciones(request, cliente_id, sucursal_id):
    """Subir archivo Excel con equipos y activos - vibraciones"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid() and request.FILES['archivo']:
            archivo = request.FILES['archivo']
            accion = form.cleaned_data['accion']
            
            # Parsear archivo
            parser = ExcelEquiposParser(archivo, sucursal)
            datos = parser.parsear()
            
            if parser.errores:
                context = {
                    'form': form,
                    'cliente': cliente,
                    'sucursal': sucursal,
                    'modulo': 'vibraciones',
                    'errores': parser.errores,
                    'titulo': 'Subir Planilla de Activos'
                }
                return render(request, 'core/upload_equipos.html', context)
            
            # Mostrar preview si es GET desde preview button
            preview = parser.obtener_preview()
            # Guardar referencia del archivo en sesión (NO guardar bytes directamente)
            import base64
            from django.core.files.uploadedfile import InMemoryUploadedFile
            
            # Convertir archivo a base64 para guardarlo en sesión (JSON-safe)
            archivo.seek(0)
            archivo_contenido = archivo.read()
            archivo_b64 = base64.b64encode(archivo_contenido).decode('utf-8')
            
            request.session['archivo_temporal_b64'] = archivo_b64
            request.session['archivo_nombre'] = archivo.name
            request.session['accion_importacion'] = accion
            context = {
                'form': form,
                'cliente': cliente,
                'sucursal': sucursal,
                'modulo': 'vibraciones',
                'preview': preview,
                'accion': accion,
                'titulo': 'Vista Previa - Subir Planilla de Activos'
            }
            return render(request, 'core/upload_equipos_preview.html', context)
    else:
        form = ExcelUploadForm()
    
    context = {
        'form': form,
        'cliente': cliente,
        'sucursal': sucursal,
        'modulo': 'vibraciones',
        'titulo': 'Subir Planilla de Activos'
    }
    return render(request, 'core/upload_equipos.html', context)


@login_required(login_url='login')
def confirmar_upload_equipos_vibraciones(request, cliente_id, sucursal_id):
    """Confirmar e importar equipos desde Excel - vibraciones"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    
    if request.method == 'POST':
        # Recuperar archivo de sesión
        if 'archivo_temporal_b64' not in request.session:
            return redirect('upload_equipos_vibraciones', cliente_id=cliente_id, sucursal_id=sucursal_id)
        
        # Recrear archivo desde sesión
        from django.core.files.uploadedfile import InMemoryUploadedFile
        import io
        import base64
        
        archivo_b64 = request.session['archivo_temporal_b64']
        archivo_contenido = base64.b64decode(archivo_b64.encode('utf-8'))
        archivo_nombre = request.session.get('archivo_nombre', 'archivo.xlsx')
        archivo = InMemoryUploadedFile(
            io.BytesIO(archivo_contenido),
            'archivo',
            archivo_nombre,
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            len(archivo_contenido),
            None
        )
        
        accion = request.POST.get('accion', request.session.get('accion_importacion', 'merge'))
        
        # Parsear e importar
        parser = ExcelEquiposParser(archivo, sucursal)
        parser.parsear()
        resultado = parser.importar(accion)
        
        # Limpiar sesión
        request.session.pop('archivo_temporal_b64', None)
        request.session.pop('archivo_nombre', None)
        request.session.pop('accion_importacion', None)
        
        context = {
            'cliente': cliente,
            'sucursal': sucursal,
            'modulo': 'vibraciones',
            'resultado': resultado,
            'titulo': 'Resultado de Importación'
        }
        return render(request, 'core/upload_equipos_resultado.html', context)
    
    return redirect('sucursales_vibraciones', cliente_id=cliente_id)


# EQUIPOS - TERMOGRAFÍAS
@login_required(login_url='login')
def equipos_termografias(request, cliente_id, sucursal_id, area_id):
    """Página de activos para un área en termografías"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    area = get_object_or_404(Area, id=area_id, sucursal=sucursal)
    
    # Obtener todos los activos del área (a través de equipos del área)
    activos = Activo.objects.filter(
        equipo__area=area,
        activo=True
    ).select_related('equipo', 'equipo__area').order_by('equipo__nombre', 'nombre')
    
    context = {
        'user': request.user,
        'cliente': cliente,
        'sucursal': sucursal,
        'area': area,
        'activos': activos,
        'modulo': 'termografias',
        'titulo': f'Todos los Activos - {area.get_nombre_display()}',
        'descripcion': 'Listado de todos los activos del área'
    }
    return render(request, 'core/termografias/activos_totales.html', context)


@login_required(login_url='login')
def crear_equipo_termografias(request, cliente_id, sucursal_id, area_id):
    """Crear equipo desde módulo de termografías"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    area = get_object_or_404(Area, id=area_id, sucursal=sucursal)
    
    if request.method == 'POST':
        form = EquipoForm(request.POST)
        if form.is_valid():
            equipo = form.save(commit=False)
            equipo.area = area
            equipo.save()
            return redirect('equipos_termografias', cliente_id=cliente_id, sucursal_id=sucursal_id, area_id=area_id)
    else:
        form = EquipoForm()
    
    context = {
        'form': form,
        'cliente': cliente,
        'sucursal': sucursal,
        'area': area,
        'modulo': 'termografias',
        'titulo': f'Nuevo Equipo - {area.get_nombre_display()}'
    }
    return render(request, 'core/equipo_form.html', context)


@login_required(login_url='login')
def editar_equipo_termografias(request, cliente_id, sucursal_id, area_id, equipo_id):
    """Editar equipo desde módulo de termografías"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    area = get_object_or_404(Area, id=area_id, sucursal=sucursal)
    equipo = get_object_or_404(Equipo, id=equipo_id, area=area)
    
    if request.method == 'POST':
        form = EquipoForm(request.POST, instance=equipo)
        if form.is_valid():
            form.save()
            return redirect('equipos_termografias', cliente_id=cliente_id, sucursal_id=sucursal_id, area_id=area_id)
    else:
        form = EquipoForm(instance=equipo)
    
    context = {
        'form': form,
        'cliente': cliente,
        'sucursal': sucursal,
        'area': area,
        'equipo': equipo,
        'modulo': 'termografias',
        'titulo': f'Editar {equipo.nombre}'
    }
    return render(request, 'core/equipo_form.html', context)


@login_required(login_url='login')
def eliminar_equipo_termografias(request, cliente_id, sucursal_id, area_id, equipo_id):
    """Eliminar equipo desde módulo de termografías"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    area = get_object_or_404(Area, id=area_id, sucursal=sucursal)
    equipo = get_object_or_404(Equipo, id=equipo_id, area=area)
    equipo.delete()
    return redirect('equipos_termografias', cliente_id=cliente_id, sucursal_id=sucursal_id, area_id=area_id)


# ACTIVOS - TERMOGRAFÍAS
@login_required(login_url='login')
def activos_termografias(request, cliente_id, sucursal_id, area_id, equipo_id):
    """Página de activos para un equipo en termografías"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    area = get_object_or_404(Area, id=area_id, sucursal=sucursal)
    equipo = get_object_or_404(Equipo, id=equipo_id, area=area)
    activos = equipo.activos.filter(activo=True).order_by('nombre')
    
    context = {
        'user': request.user,
        'cliente': cliente,
        'sucursal': sucursal,
        'area': area,
        'equipo': equipo,
        'activos': activos,
        'modulo': 'termografias',
        'titulo': f'Activos - {equipo.nombre}',
        'descripcion': 'Gestiona los componentes y motores del equipo'
    }
    return render(request, 'core/termografias/activos_totales.html', context)


@login_required(login_url='login')
def crear_activo_termografias(request, cliente_id, sucursal_id, area_id, equipo_id):
    """Crear activo desde módulo de termografías"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    area = get_object_or_404(Area, id=area_id, sucursal=sucursal)
    equipo = get_object_or_404(Equipo, id=equipo_id, area=area)
    
    if request.method == 'POST':
        form = ActivoForm(request.POST)
        if form.is_valid():
            activo = form.save(commit=False)
            activo.equipo = equipo
            activo.save()
            return redirect('activos_termografias', cliente_id=cliente_id, sucursal_id=sucursal_id, area_id=area_id, equipo_id=equipo_id)
    else:
        form = ActivoForm()
    
    context = {
        'form': form,
        'cliente': cliente,
        'sucursal': sucursal,
        'area': area,
        'equipo': equipo,
        'modulo': 'termografias',
        'titulo': f'Nuevo Activo - {equipo.nombre}'
    }
    return render(request, 'core/activo_form.html', context)


@login_required(login_url='login')
def editar_activo_termografias(request, cliente_id, sucursal_id, area_id, equipo_id, activo_id):
    """Editar activo desde módulo de termografías"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    area = get_object_or_404(Area, id=area_id, sucursal=sucursal)
    equipo = get_object_or_404(Equipo, id=equipo_id, area=area)
    activo = get_object_or_404(Activo, id=activo_id, equipo=equipo)
    
    if request.method == 'POST':
        form = ActivoForm(request.POST, instance=activo)
        if form.is_valid():
            form.save()
            return redirect('activos_termografias', cliente_id=cliente_id, sucursal_id=sucursal_id, area_id=area_id, equipo_id=equipo_id)
    else:
        form = ActivoForm(instance=activo)
    
    context = {
        'form': form,
        'cliente': cliente,
        'sucursal': sucursal,
        'area': area,
        'equipo': equipo,
        'activo': activo,
        'modulo': 'termografias',
        'titulo': f'Editar {activo.nombre}'
    }
    return render(request, 'core/activo_form.html', context)


@login_required(login_url='login')
def eliminar_activo_termografias(request, cliente_id, sucursal_id, area_id, equipo_id, activo_id):
    """Eliminar activo desde módulo de termografías"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    area = get_object_or_404(Area, id=area_id, sucursal=sucursal)
    equipo = get_object_or_404(Equipo, id=equipo_id, area=area)
    activo = get_object_or_404(Activo, id=activo_id, equipo=equipo)
    activo.delete()
    return redirect('activos_termografias', cliente_id=cliente_id, sucursal_id=sucursal_id, area_id=area_id, equipo_id=equipo_id)


# EDITAR/ELIMINAR ACTIVOS DESDE LISTADO TOTAL - TERMOGRAFÍAS
@login_required(login_url='login')
def editar_activo_total_termografias(request, cliente_id, sucursal_id, activo_id):
    """Editar activo desde listado total de termografías"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    activo = get_object_or_404(Activo, id=activo_id, equipo__area__sucursal=sucursal)
    
    if request.method == 'POST':
        form = ActivoForm(request.POST, instance=activo)
        if form.is_valid():
            form.save()
            return redirect('activos_totales_termografias', cliente_id=cliente_id, sucursal_id=sucursal_id)
    else:
        form = ActivoForm(instance=activo)
    
    context = {
        'form': form,
        'cliente': cliente,
        'sucursal': sucursal,
        'activo': activo,
        'modulo': 'termografias',
        'titulo': f'Editar {activo.nombre}'
    }
    return render(request, 'core/activo_form.html', context)


@login_required(login_url='login')
def eliminar_activo_total_termografias(request, cliente_id, sucursal_id, activo_id):
    """Eliminar activo desde listado total de termografías"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    activo = get_object_or_404(Activo, id=activo_id, equipo__area__sucursal=sucursal)
    activo.delete()
    return redirect('activos_totales_termografias', cliente_id=cliente_id, sucursal_id=sucursal_id)


# EDITAR/ELIMINAR ACTIVOS DESDE LISTADO TOTAL - VIBRACIONES
@login_required(login_url='login')
def editar_activo_total_vibraciones(request, cliente_id, sucursal_id, activo_id):
    """Editar activo desde listado total de vibraciones"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    activo = get_object_or_404(Activo, id=activo_id, equipo__area__sucursal=sucursal)
    
    if request.method == 'POST':
        form = ActivoForm(request.POST, instance=activo)
        if form.is_valid():
            form.save()
            return redirect('equipos_totales_vibraciones', cliente_id=cliente_id, sucursal_id=sucursal_id)
    else:
        form = ActivoForm(instance=activo)
    
    context = {
        'form': form,
        'cliente': cliente,
        'sucursal': sucursal,
        'activo': activo,
        'modulo': 'vibraciones',
        'titulo': f'Editar {activo.nombre}'
    }
    return render(request, 'core/activo_form.html', context)


@login_required(login_url='login')
def eliminar_activo_total_vibraciones(request, cliente_id, sucursal_id, activo_id):
    """Eliminar activo desde listado total de vibraciones"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    activo = get_object_or_404(Activo, id=activo_id, equipo__area__sucursal=sucursal)
    activo.delete()
    return redirect('equipos_totales_vibraciones', cliente_id=cliente_id, sucursal_id=sucursal_id)


# UPLOAD EXCEL - TERMOGRAFÍAS
@login_required(login_url='login')
def upload_equipos_termografias(request, cliente_id, sucursal_id):
    """Subir archivo Excel con equipos y activos - termografías"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid() and request.FILES['archivo']:
            archivo = request.FILES['archivo']
            accion = form.cleaned_data['accion']
            
            # Parsear archivo
            parser = ExcelEquiposParser(archivo, sucursal)
            datos = parser.parsear()
            
            if parser.errores:
                context = {
                    'form': form,
                    'cliente': cliente,
                    'sucursal': sucursal,
                    'modulo': 'termografias',
                    'errores': parser.errores,
                    'titulo': 'Subir Planilla de Activos'
                }
                return render(request, 'core/upload_equipos.html', context)
            
            # Mostrar preview
            preview = parser.obtener_preview()
            # Guardar referencia del archivo en sesión (NO guardar bytes directamente)
            import base64
            from django.core.files.uploadedfile import InMemoryUploadedFile
            
            # Convertir archivo a base64 para guardarlo en sesión (JSON-safe)
            archivo.seek(0)
            archivo_contenido = archivo.read()
            archivo_b64 = base64.b64encode(archivo_contenido).decode('utf-8')
            
            request.session['archivo_temporal_b64'] = archivo_b64
            request.session['archivo_nombre'] = archivo.name
            request.session['accion_importacion'] = accion
            context = {
                'form': form,
                'cliente': cliente,
                'sucursal': sucursal,
                'modulo': 'termografias',
                'preview': preview,
                'accion': accion,
                'titulo': 'Vista Previa - Subir Planilla de Activos'
            }
            return render(request, 'core/upload_equipos_preview.html', context)
    else:
        form = ExcelUploadForm()
    
    context = {
        'form': form,
        'cliente': cliente,
        'sucursal': sucursal,
        'modulo': 'termografias',
        'titulo': 'Subir Planilla de Activos'
    }
    return render(request, 'core/upload_equipos.html', context)


@login_required(login_url='login')
def confirmar_upload_equipos_termografias(request, cliente_id, sucursal_id):
    """Confirmar e importar equipos desde Excel - termografías"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    
    if request.method == 'POST':
        # Recuperar archivo de sesión
        if 'archivo_temporal_b64' not in request.session:
            return redirect('upload_equipos_termografias', cliente_id=cliente_id, sucursal_id=sucursal_id)
        
        # Recrear archivo desde sesión
        from django.core.files.uploadedfile import InMemoryUploadedFile
        import io
        import base64
        
        archivo_b64 = request.session['archivo_temporal_b64']
        archivo_contenido = base64.b64decode(archivo_b64.encode('utf-8'))
        archivo_nombre = request.session.get('archivo_nombre', 'archivo.xlsx')
        archivo = InMemoryUploadedFile(
            io.BytesIO(archivo_contenido),
            'archivo',
            archivo_nombre,
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            len(archivo_contenido),
            None
        )
        
        accion = request.POST.get('accion', request.session.get('accion_importacion', 'merge'))
        
        # Parsear e importar
        parser = ExcelEquiposParser(archivo, sucursal)
        parser.parsear()
        resultado = parser.importar(accion)
        
        # Limpiar sesión
        request.session.pop('archivo_temporal_b64', None)
        request.session.pop('archivo_nombre', None)
        request.session.pop('accion_importacion', None)
        
        context = {
            'cliente': cliente,
            'sucursal': sucursal,
            'modulo': 'termografias',
            'resultado': resultado,
            'titulo': 'Resultado de Importación'
        }
        return render(request, 'core/upload_equipos_resultado.html', context)
    
    return redirect('sucursales_termografias', cliente_id=cliente_id)


@require_http_methods(["POST"])
@login_required
def actualizar_estado_equipo(request, equipo_id):
    """Actualiza el estado de un equipo via AJAX"""
    try:
        equipo = get_object_or_404(Equipo, id=equipo_id)
        nuevo_estado = request.POST.get('estado')
        
        if nuevo_estado in dict(Equipo.ESTADO_CHOICES):
            equipo.estado = nuevo_estado
            equipo.save()
            return JsonResponse({
                'success': True,
                'estado': equipo.get_estado_display()
            })
        
        return JsonResponse({'success': False, 'error': 'Estado inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_http_methods(["POST"])
@login_required
def actualizar_estado_activo(request, activo_id):
    """Actualiza el estado de un activo via AJAX"""
    try:
        activo = get_object_or_404(Activo, id=activo_id)
        nuevo_estado = request.POST.get('estado')
        
        if nuevo_estado in dict(Activo.ESTADO_CHOICES):
            activo.estado = nuevo_estado
            activo.save()
            return JsonResponse({
                'success': True,
                'estado': activo.get_estado_display()
            })
        
        return JsonResponse({'success': False, 'error': 'Estado inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_http_methods(["POST"])
@login_required
def actualizar_observacion_equipo(request, equipo_id):
    """Actualiza la observación de un equipo via AJAX"""
    try:
        equipo = get_object_or_404(Equipo, id=equipo_id)
        observacion = request.POST.get('observacion', '')
        
        equipo.observaciones = observacion
        equipo.save()
        return JsonResponse({
            'success': True,
            'observacion': equipo.observaciones
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_http_methods(["POST"])
@login_required
def actualizar_observacion_activo(request, activo_id):
    """Actualiza la observación de un activo via AJAX"""
    try:
        activo = get_object_or_404(Activo, id=activo_id)
        observacion = request.POST.get('observacion', '')
        
        activo.observaciones = observacion
        activo.save()
        return JsonResponse({
            'success': True,
            'observacion': activo.observaciones
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def actualizar_descripcion_activo(request, activo_id):
    """Actualiza la descripción de un activo via AJAX"""
    try:
        activo = get_object_or_404(Activo, id=activo_id)
        descripcion = request.POST.get('descripcion', '')
        
        activo.descripcion = descripcion
        activo.save()
        return JsonResponse({
            'success': True,
            'descripcion': activo.descripcion
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_http_methods(["POST"])
@login_required
def agregar_muestra_vibracion(request, activo_id):
    """Agrega o actualiza una muestra de vibraciones para un activo"""
    try:
        from datetime import datetime
        
        activo = get_object_or_404(Activo, id=activo_id)
        
        # Obtener parámetros
        fecha_str = request.POST.get('fecha', '')
        velocidad_rms = request.POST.get('velocidad_rms', 0)
        aceleracion = request.POST.get('aceleracion', 0)
        resultado = request.POST.get('resultado', 'sin_medicion')
        observaciones = request.POST.get('observaciones', '')
        descripcion = request.POST.get('descripcion', '')
        
        if not fecha_str:
            return JsonResponse({'success': False, 'error': 'Fecha requerida'}, status=400)
        
        # Validar resultado
        resultado_choices = dict(VibracionesAnalisis.RESULTADO_CHOICES)
        if resultado not in resultado_choices:
            resultado = 'sin_medicion'
        
        # Convertir fecha
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        
        # Actualizar descripción del activo si se proporcionó
        if descripcion:
            activo.descripcion = descripcion
            activo.save()
        
        # Crear o actualizar muestra (en caso de que ya exista para esa fecha)
        muestra, created = VibracionesAnalisis.objects.update_or_create(
            activo=activo,
            fecha_muestreo=fecha,
            defaults={
                'velocidad_rms': float(velocidad_rms) if velocidad_rms else 0,
                'aceleracion': float(aceleracion) if aceleracion else 0,
                'resultado': resultado,
                'observaciones': observaciones
            }
        )
        
        return JsonResponse({
            'success': True,
            'muestra_id': muestra.id,
            'fecha': muestra.fecha_muestreo.strftime('%Y-%m-%d'),
            'mensaje': 'Muestra de vibraciones guardada exitosamente'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def guardar_fecha_muestreo(request, activo_id):
    """Guarda o actualiza la fecha de muestreo de un activo via AJAX"""
    try:
        activo = get_object_or_404(Activo, id=activo_id)
        fecha_str = request.POST.get('fecha', '')
        
        if not fecha_str:
            return JsonResponse({'success': False, 'error': 'Fecha requerida'}, status=400)
        
        from datetime import datetime
        # Convertir string de fecha a objeto date
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        
        # Crear o actualizar el registro de muestreo
        muestreo, created = MuestreoActivo.objects.get_or_create(
            activo=activo,
            fecha_muestreo=fecha
        )
        
        return JsonResponse({
            'success': True,
            'fecha': muestreo.fecha_muestreo.strftime('%Y-%m-%d'),
            'mensaje': 'Muestreo registrado exitosamente'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def obtener_ultima_fecha_muestreo(request, activo_id):
    """Obtiene la última fecha de muestreo de un activo"""
    try:
        activo = get_object_or_404(Activo, id=activo_id)
        muestreo = activo.muestreos.first()  # El primero porque ordering es -fecha_muestreo
        
        if muestreo:
            return JsonResponse({
                'success': True,
                'fecha': muestreo.fecha_muestreo.strftime('%Y-%m-%d')
            })
        else:
            return JsonResponse({
                'success': False,
                'fecha': None,
                'mensaje': 'Sin muestreos registrados'
            })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_http_methods(["POST"])
@login_required(login_url='login')
def subir_foto_termica(request, activo_id):
    """Sube una foto térmica para un activo y la analiza automáticamente"""
    import logging
    logger = logging.getLogger(__name__)
    from .analisis_termico import AnalizadorTermico
    
    try:
        from .models import AnalisisTermico
        
        activo = get_object_or_404(Activo, id=activo_id)
        
        if 'foto' not in request.FILES:
            return JsonResponse({'success': False, 'error': 'No se proporcionó archivo'}, status=400)
        
        # Verificar si es una nueva muestra (para histórico)
        es_nueva_muestra = request.POST.get('nueva_muestra', 'false').lower() == 'true'
        logger.info(f"Subida de foto - Nueva muestra: {es_nueva_muestra}")
        
        archivo = request.FILES['foto']
        logger.info(f"Archivo recibido: {archivo.name}, tipo: {archivo.content_type}, tamaño: {archivo.size}")
        
        # Validar que sea una imagen
        if not archivo.content_type.startswith('image/'):
            return JsonResponse({'success': False, 'error': 'El archivo debe ser una imagen'}, status=400)
        
        # Si es nueva muestra, guardar análisis anterior
        analisis_anterior = None
        if es_nueva_muestra:
            try:
                analisis_anterior = AnalisisTermico.objects.get(activo=activo)
                logger.info(f"✅ Análisis anterior preservado en histórico")
            except AnalisisTermico.DoesNotExist:
                logger.info(f"ℹ️ No hay análisis anterior para preservar")
        
        # Eliminar foto anterior si existe (pero preservar análisis si es nueva muestra)
        if activo.foto_termica:
            activo.foto_termica.delete()
        
        # Guardar nueva foto
        activo.foto_termica = archivo
        activo.save()
        logger.info(f"✅ Foto guardada correctamente")
        
        # Intentar analizar - si falla, devolvemos la foto sin análisis
        resultado_analisis = None
        try:
            analizador = AnalizadorTermico()
            logger.info(f">>> LLAMANDO analizar_imagen({activo.foto_termica})")
            resultado_analisis = analizador.analizar_imagen(activo.foto_termica)
            logger.info(f">>> RESULTADO COMPLETO: {resultado_analisis}")
            print(f">>> RESULTADO COMPLETO (PRINT): {resultado_analisis}")
        except Exception as ocr_error:
            logger.error(f">>> EXCEPCION EN OCR: {str(ocr_error)}", exc_info=True)
            print(f">>> EXCEPCION EN OCR (PRINT): {str(ocr_error)}")
            # Sin OCR, devolver valores por defecto
            resultado_analisis = None
        
        # Si OCR falló, retornar con análisis null pero foto guardada
        if resultado_analisis is None or 'error' in resultado_analisis:
            logger.info(f"✅ Foto subida. Ingresa los valores manualmente en el modal.")
            return JsonResponse({
                'success': True,
                'foto_url': activo.foto_termica.url,
                'mensaje': 'Foto subida correctamente. Por favor ingresa los valores manualmente.',
                'error_analisis': 'OCR no disponible - Ingresa los valores de temperatura en el modal',
                'analisis': None
            })
        
        # 🔄 IMPORTANTE: Ahora usamos ForeignKey en lugar de OneToOne
        # Esto permite crear MÚLTIPLES AnalisisTermico por Activo (histórico)
        # Siempre creamos un nuevo registro en lugar de actualizar
        analisis = AnalisisTermico.objects.create(
            activo=activo,
            temperatura_promedio=resultado_analisis['temperatura_promedio'],
            temperatura_maxima=resultado_analisis['temperatura_maxima'],
            temperatura_minima=resultado_analisis['temperatura_minima'],
            rango_minimo=resultado_analisis['rango_minimo'],
            rango_maximo=resultado_analisis['rango_maximo'],
            porcentaje_zona_critica=resultado_analisis['porcentaje_zona_critica'],
            porcentaje_zona_alerta=resultado_analisis['porcentaje_zona_alerta'],
            porcentaje_zona_caliente=resultado_analisis['porcentaje_zona_caliente'],
            estado=resultado_analisis['estado'],
        )
        creado = True
        logger.info(f"✅ Nuevo AnalisisTermico creado (ID: {analisis.id}) para activo {activo_id}")
        logger.info(f"   Temperatura máxima: {resultado_analisis['temperatura_maxima']}°C")
        logger.info(f"   Estado: {resultado_analisis['estado']}")
        
        # Actualizar el estado del Activo con el estado del análisis
        activo.estado = resultado_analisis['estado']
        activo.save()
        logger.info(f"✅ Estado del activo {activo_id} actualizado a: {resultado_analisis['estado']}")
        
        response_data = {
            'success': True,
            'foto_url': activo.foto_termica.url,
            'mensaje': 'Foto subida y analizada correctamente',
            'analisis': {
                'temperatura_promedio': resultado_analisis['temperatura_promedio'],
                'temperatura_maxima': resultado_analisis['temperatura_maxima'],
                'temperatura_minima': resultado_analisis['temperatura_minima'],
                'porcentaje_zona_critica': resultado_analisis['porcentaje_zona_critica'],
                'porcentaje_zona_alerta': resultado_analisis['porcentaje_zona_alerta'],
                'porcentaje_zona_caliente': resultado_analisis['porcentaje_zona_caliente'],
                'estado': resultado_analisis['estado'],
                'mensaje': resultado_analisis['mensaje']
            }
        }
        logger.info(f"📤 Enviando respuesta JSON con análisis: {response_data}")
        return JsonResponse(response_data)
    except Exception as e:
        logger.error(f"Error subiendo foto térmica: {str(e)}", exc_info=True)
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_http_methods(["POST"])
@login_required(login_url='login')
@require_http_methods(["POST"])
@login_required(login_url='login')
def eliminar_foto_termica(request, activo_id):
    """Elimina la foto térmica y análisis de un activo, reseteando la medición"""
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        from .models import AnalisisTermico
        
        activo = get_object_or_404(Activo, id=activo_id)
        logger.info(f"🗑️ Eliminando foto térmica del activo {activo_id}")
        
        # Eliminar análisis asociado
        try:
            analisis = AnalisisTermico.objects.get(activo=activo)
            analisis.delete()
            logger.info(f"✅ Análisis eliminado")
        except AnalisisTermico.DoesNotExist:
            logger.info(f"ℹ️ No hay análisis para eliminar")
        
        # Eliminar archivo de foto
        if activo.foto_termica:
            archivo_path = activo.foto_termica.path if hasattr(activo.foto_termica, 'path') else None
            activo.foto_termica.delete()
            logger.info(f"✅ Archivo de foto eliminado")
        
        # Resetear estado del activo
        activo.estado = 'sin_medicion'
        activo.save()
        logger.info(f"✅ Estado del activo reseteado a: sin_medicion")
        
        return JsonResponse({
            'success': True,
            'mensaje': 'Foto térmica y análisis eliminados correctamente'
        })
    
    except Exception as e:
        logger.error(f"Error eliminando foto térmica: {str(e)}", exc_info=True)
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_http_methods(["GET"])
@login_required(login_url='/login/')
def obtener_analisis_termico(request, activo_id):
    """Obtiene el análisis térmico más reciente para un activo"""
    try:
        from .models import AnalisisTermico
        import logging
        
        logger = logging.getLogger(__name__)
        
        activo = get_object_or_404(Activo, id=activo_id)
        
        # Obtener el análisis más reciente (el último creado)
        analisis = activo.analisis_termicos.latest('creado')
        
        logger.info(f"✅ Análisis obtenido para activo {activo_id} (ID: {analisis.id})")
        
        # Construir respuesta con valores convertidos a float para evitar errores de serialización
        foto_url = ''
        if activo.foto_termica:
            foto_url = activo.foto_termica.url
        
        zona_caliente = float(analisis.porcentaje_zona_critica) + float(analisis.porcentaje_zona_alerta)
        
        return JsonResponse({
            'success': True,
            'foto_url': foto_url,
            'analisis': {
                'temperatura_promedio': float(analisis.temperatura_promedio),
                'temperatura_maxima': float(analisis.temperatura_maxima),
                'temperatura_minima': float(analisis.temperatura_minima),
                'porcentaje_zona_critica': float(analisis.porcentaje_zona_critica),
                'porcentaje_zona_alerta': float(analisis.porcentaje_zona_alerta),
                'porcentaje_zona_caliente': zona_caliente,
                'estado': analisis.estado,
                'mensaje': f"{analisis.estado.upper()}: {zona_caliente:.1f}% de zona caliente detectada",
                'zona_bueno_min': float(analisis.zona_bueno_min),
                'zona_bueno_max': float(analisis.zona_bueno_max),
                'zona_alarma_min': float(analisis.zona_alarma_min),
                'zona_alarma_max': float(analisis.zona_alarma_max),
                'zona_emergencia_min': float(analisis.zona_emergencia_min),
                'zona_emergencia_max': float(analisis.zona_emergencia_max)
            }
        })
    except AnalisisTermico.DoesNotExist:
        logger.warning(f"❌ No existe análisis para activo {activo_id}")
        return JsonResponse({
            'success': False,
            'error': 'No hay análisis disponible para este activo'
        }, status=404)
    except Exception as e:
        logger.error(f"Error obteniendo análisis térmico: {str(e)}", exc_info=True)
        return JsonResponse({'success': False, 'error': f'Error del servidor: {str(e)}'}, status=500)


@login_required(login_url='/login/')
@require_http_methods(["POST"])
def guardar_temperaturas_activo(request, activo_id):
    """Guarda los valores de temperatura editados por el usuario"""
    try:
        import json
        import logging
        from .models import AnalisisTermico, Activo
        
        logger = logging.getLogger(__name__)
        
        # Obtener el activo
        activo = get_object_or_404(Activo, id=activo_id)
        
        # Parsear JSON
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            logger.error("Error decodificando JSON")
            return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)
        
        temperatura_promedio = float(data.get('temperatura_promedio', 0))
        temperatura_minima = float(data.get('temperatura_minima', 0))
        temperatura_maxima = float(data.get('temperatura_maxima', 0))
        
        # Obtener los rangos de cada zona
        zona_bueno_min = float(data.get('zona_bueno_min', 20))
        zona_bueno_max = float(data.get('zona_bueno_max', 50))
        zona_alarma_min = float(data.get('zona_alarma_min', 50))
        zona_alarma_max = float(data.get('zona_alarma_max', 65))
        zona_emergencia_min = float(data.get('zona_emergencia_min', 65))
        zona_emergencia_max = float(data.get('zona_emergencia_max', 100))
        
        logger.info(f"Guardando temperaturas para activo {activo_id}: Prom={temperatura_promedio}, Min={temperatura_minima}, Max={temperatura_maxima}")
        
        # Obtener o crear el análisis térmico
        analisis, created = AnalisisTermico.objects.get_or_create(activo=activo)
        
        # Actualizar los valores de temperatura detectada
        analisis.temperatura_promedio = temperatura_promedio
        analisis.temperatura_minima = temperatura_minima
        analisis.temperatura_maxima = temperatura_maxima
        
        # Actualizar rangos de operación por zona
        analisis.zona_bueno_min = zona_bueno_min
        analisis.zona_bueno_max = zona_bueno_max
        analisis.zona_alarma_min = zona_alarma_min
        analisis.zona_alarma_max = zona_alarma_max
        analisis.zona_emergencia_min = zona_emergencia_min
        analisis.zona_emergencia_max = zona_emergencia_max
        
        # Actualizar rangos antiguos también (compatibilidad)
        analisis.rango_minimo = temperatura_minima
        analisis.rango_maximo = temperatura_maxima
        
        # Determinar estado basado en la T° detectada vs los rangos definidos
        # Prioridad: EMERGENCIA > ALARMA > BUENO
        if zona_emergencia_min <= temperatura_promedio <= zona_emergencia_max:
            analisis.estado = 'emergencia'
        elif zona_alarma_min <= temperatura_promedio <= zona_alarma_max:
            analisis.estado = 'alarma'
        elif zona_bueno_min <= temperatura_promedio <= zona_bueno_max:
            analisis.estado = 'bueno'
        else:
            # Si está fuera de todos los rangos, determinar cuál es el más cercano
            if temperatura_promedio < zona_bueno_min or temperatura_promedio > zona_emergencia_max:
                analisis.estado = 'emergencia'
            else:
                analisis.estado = 'alarma'
        
        analisis.save()
        
        # 🔴 IMPORTANTE: Actualizar también el estado del Activo para que se refleje en la tabla
        activo.estado = analisis.estado
        activo.save()
        
        logger.info(f"✅ Temperaturas guardadas exitosamente para activo {activo_id}, estado={analisis.estado}")
        
        return JsonResponse({
            'success': True,
            'message': 'Temperaturas guardadas correctamente',
            'analisis': {
                'temperatura_promedio': float(analisis.temperatura_promedio),
                'temperatura_maxima': float(analisis.temperatura_maxima),
                'temperatura_minima': float(analisis.temperatura_minima),
                'estado': analisis.estado,
                'zonas': {
                    'bueno': {'min': float(analisis.zona_bueno_min), 'max': float(analisis.zona_bueno_max)},
                    'alarma': {'min': float(analisis.zona_alarma_min), 'max': float(analisis.zona_alarma_max)},
                    'emergencia': {'min': float(analisis.zona_emergencia_min), 'max': float(analisis.zona_emergencia_max)}
                }
            }
        })
        
    except json.JSONDecodeError:
        logger.error("Error decodificando JSON")
        return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)
    except Exception as e:
        logger.error(f"Error guardando temperaturas: {str(e)}", exc_info=True)
        return JsonResponse({'success': False, 'error': f'Error del servidor: {str(e)}'}, status=500)


@login_required(login_url='/login/')
def configuracion(request):
    """Vista de configuración del usuario"""
    return render(request, 'core/configuracion.html')


@login_required(login_url='/login/')
def upload_profile_photo(request):
    """Maneja la carga de foto de perfil"""
    if request.method == 'POST':
        try:
            photo_file = request.FILES.get('photo')
            
            if not photo_file:
                return JsonResponse({'success': False, 'error': 'No se recibió archivo'}, status=400)
            
            # Validar tamaño
            if photo_file.size > 5 * 1024 * 1024:  # 5MB
                return JsonResponse({'success': False, 'error': 'Archivo muy grande'}, status=400)
            
            # Validar tipo
            if photo_file.content_type not in ['image/jpeg', 'image/png', 'image/gif']:
                return JsonResponse({'success': False, 'error': 'Tipo de archivo no permitido'}, status=400)
            
            # Obtener o crear el perfil del usuario
            from .models import UserProfile
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            
            # Guardar la foto en el perfil
            profile.photo = photo_file
            profile.save()
            
            return JsonResponse({
                'success': True, 
                'message': 'Foto subida exitosamente',
                'photo_url': profile.photo.url
            })
        
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)


@login_required(login_url='/login/')
def save_config(request):
    """Guarda la configuración del usuario"""
    if request.method == 'POST':
        try:
            user = request.user
            
            # Actualizar datos del usuario
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.email = request.POST.get('email', user.email)
            
            user.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Configuración guardada exitosamente'
            })
        
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)


@login_required(login_url='login')
def subir_logo_cliente(request, cliente_id):
    """API para subir el logo del cliente"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)
    
    try:
        cliente = get_object_or_404(Cliente, id=cliente_id)
        
        if 'logo' not in request.FILES:
            return JsonResponse({'success': False, 'error': 'No se proporcionó archivo'}, status=400)
        
        archivo = request.FILES['logo']
        
        # Validar que sea una imagen
        if not archivo.content_type.startswith('image/'):
            return JsonResponse({'success': False, 'error': 'El archivo debe ser una imagen'}, status=400)
        
        # Validar tamaño máximo (2MB)
        if archivo.size > 2 * 1024 * 1024:
            return JsonResponse({'success': False, 'error': 'El archivo es demasiado grande (máximo 2MB)'}, status=400)
        
        # Eliminar archivo anterior si existe
        if cliente.logo:
            cliente.logo.delete()
        
        # Guardar nuevo archivo
        cliente.logo = archivo
        cliente.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Logo subido exitosamente',
            'image_url': cliente.logo.url
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required(login_url='login')
def subir_plano_planta(request, sucursal_id):
    """API para subir el plano de la planta"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)
    
    try:
        sucursal = get_object_or_404(Sucursal, id=sucursal_id)
        
        if 'plano_planta' not in request.FILES:
            return JsonResponse({'success': False, 'error': 'No se proporcionó archivo'}, status=400)
        
        archivo = request.FILES['plano_planta']
        
        # Validar que sea una imagen
        if not archivo.content_type.startswith('image/'):
            return JsonResponse({'success': False, 'error': 'El archivo debe ser una imagen'}, status=400)
        
        # Validar tamaño máximo (5MB)
        if archivo.size > 5 * 1024 * 1024:
            return JsonResponse({'success': False, 'error': 'El archivo es demasiado grande (máximo 5MB)'}, status=400)
        
        # Eliminar archivo anterior si existe
        if sucursal.plano_planta:
            sucursal.plano_planta.delete()
        
        # Guardar nuevo archivo
        sucursal.plano_planta = archivo
        sucursal.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Plano de planta subido exitosamente',
            'image_url': sucursal.plano_planta.url
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_http_methods(["POST"])
@login_required(login_url='login')
def guardar_fecha_muestreo_equipo(request, equipo_id):
    """Guarda o actualiza la fecha de muestreo de un equipo via AJAX"""
    try:
        equipo = get_object_or_404(Equipo, id=equipo_id)
        fecha_str = request.POST.get('fecha', '')
        
        if not fecha_str:
            return JsonResponse({'success': False, 'error': 'Fecha requerida'}, status=400)
        
        from datetime import datetime
        # Convertir string de fecha a objeto date
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        
        # Crear o actualizar el registro de muestreo
        muestreo, created = MuestreoEquipo.objects.get_or_create(
            equipo=equipo,
            fecha_muestreo=fecha
        )
        
        return JsonResponse({
            'success': True,
            'fecha': muestreo.fecha_muestreo.strftime('%Y-%m-%d'),
            'mensaje': 'Muestreo registrado exitosamente'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_http_methods(["GET"])
@login_required(login_url='login')
def obtener_ultima_fecha_muestreo_equipo(request, equipo_id):
    """Obtiene la última fecha de muestreo de un equipo"""
    try:
        equipo = get_object_or_404(Equipo, id=equipo_id)
        muestreo = equipo.muestreos.first()  # El primero porque ordering es -fecha_muestreo
        
        if muestreo:
            return JsonResponse({
                'success': True,
                'fecha': muestreo.fecha_muestreo.strftime('%Y-%m-%d')
            })
        else:
            return JsonResponse({
                'success': False,
                'fecha': None,
                'mensaje': 'Sin muestreos registrados'
            })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@api_view(["GET"])
def health(request):
    return Response({"status": "ok", "service": "vyc-predictivo-cloud"})


# ============================================================================
# VISTAS PARA HISTÓRICO DE ANÁLISIS - VIBRACIONES
# ============================================================================

@login_required(login_url='login')
def historico_vibraciones(request, cliente_id, sucursal_id):
    """Vista del histórico de análisis de vibraciones - último análisis por activo"""
    from django.db.models import Case, When
    
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    
    # Obtener todos los activos de la sucursal con su último análisis
    # Ordenar por área (aserradero, elaborado, caldera), luego equipo, luego activo
    activos = Activo.objects.filter(
        equipo__area__sucursal=sucursal,
        activo=True
    ).select_related(
        'equipo',
        'equipo__area'
    ).annotate(
        area_orden=Case(
            When(equipo__area__nombre='aserradero', then=0),
            When(equipo__area__nombre='elaborado', then=1),
            When(equipo__area__nombre='caldera', then=2),
            default=3,
            output_field=models.IntegerField()
        )
    ).order_by('area_orden', 'equipo__nombre', 'nombre')
    
    # Construir lista de activos con su último análisis
    datos_historico = []
    ultima_fecha = None
    
    for activo in activos:
        # Obtener el último análisis de vibraciones de este activo
        ultimo_analisis = VibracionesAnalisis.objects.filter(
            activo=activo
        ).order_by('-fecha_muestreo').first()
        
        fila = {
            'numero': len(datos_historico) + 1,
            'area': activo.equipo.area,
            'equipo': activo.equipo,
            'activo': activo,
            'ultimo_analisis': ultimo_analisis
        }
        
        # Guardar la fecha más reciente para mostrar en el encabezado
        if ultimo_analisis and (ultima_fecha is None or ultimo_analisis.fecha_muestreo > ultima_fecha):
            ultima_fecha = ultimo_analisis.fecha_muestreo
        
        datos_historico.append(fila)
    
    # Calcular estadísticas
    equipos_count = Equipo.objects.filter(area__sucursal=sucursal, activo=True).distinct().count()
    activos_count = len(datos_historico)
    
    context = {
        'user': request.user,
        'cliente': cliente,
        'sucursal': sucursal,
        'modulo': 'vibraciones',
        'titulo': f'Histórico de Vibraciones - {sucursal.nombre}',
        'descripcion': 'Visualiza el historial de análisis de todos los activos',
        'datos_historico': datos_historico,
        'ultima_fecha': ultima_fecha,
        'total_equipos': equipos_count,
        'total_activos': activos_count,
    }
    return render(request, 'core/vibraciones/historico.html', context)


# ============================================================================
# VISTAS PARA HISTÓRICO DE ANÁLISIS - TERMOGRAFÍAS
# ============================================================================

@login_required(login_url='login')
def historico_termografias(request, cliente_id, sucursal_id):
    """Vista del histórico de análisis de termografías con tabla de fechas"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    
    # Obtener todos los activos de la sucursal
    activos = Activo.objects.filter(
        equipo__area__sucursal=sucursal,
        activo=True
    ).select_related(
        'equipo',
        'equipo__area'
    ).order_by('equipo__area__nombre', 'equipo__nombre', 'nombre')
    
    # Obtener todas las fechas de análisis únicos de todos los activos
    fechas = TermografiaAnalisis.objects.filter(
        activo__equipo__area__sucursal=sucursal
    ).values_list('fecha_muestreo', flat=True).distinct().order_by('-fecha_muestreo')
    
    # Construir matriz: activo -> fecha -> análisis
    datos_historico = []
    for activo in activos:
        fila = {
            'activo': activo,
            'area': activo.equipo.area,
            'equipo': activo.equipo,
            'analisis_por_fecha': {}
        }
        
        # Para cada fecha, obtener el análisis de este activo
        for fecha in fechas:
            try:
                analisis = TermografiaAnalisis.objects.get(
                    activo=activo,
                    fecha_muestreo=fecha
                )
                fila['analisis_por_fecha'][fecha] = analisis
            except TermografiaAnalisis.DoesNotExist:
                fila['analisis_por_fecha'][fecha] = None
        
        datos_historico.append(fila)
    
    # Serializar datos para JSON (para Chart.js)
    import json
    from decimal import Decimal
    
    fechas_list = [str(f) for f in fechas]
    
    # Convertir datos_historico a estructura serializable
    datos_json = []
    for item in datos_historico:
        analisis_json = {}
        for fecha, analisis in item['analisis_por_fecha'].items():
            if analisis:
                analisis_json[str(fecha)] = {
                    'temperatura_maxima': float(analisis.temperatura_maxima) if analisis.temperatura_maxima else 0,
                    'temperatura_minima': float(analisis.temperatura_minima) if analisis.temperatura_minima else 0,
                    'resultado': analisis.resultado,
                }
            else:
                analisis_json[str(fecha)] = None
        
        datos_json.append({
            'activo': {
                'id': item['activo'].id,
                'nombre': item['activo'].nombre,
            },
            'equipo': {
                'id': item['equipo'].id,
                'nombre': item['equipo'].nombre,
            },
            'area': {
                'id': item['area'].id,
                'nombre': item['area'].nombre,
            },
            'analisis_por_fecha': analisis_json
        })
    
    context = {
        'user': request.user,
        'cliente': cliente,
        'sucursal': sucursal,
        'modulo': 'termografias',
        'titulo': f'Histórico de Termografías - {sucursal.nombre}',
        'descripcion': 'Visualiza el historial de todos los análisis de termografías',
        'datos_historico': datos_historico,
        'fechas': fechas,
        'datos_historico_json': json.dumps(datos_json),
        'fechas_json': json.dumps(fechas_list),
    }
    return render(request, 'core/termografias/historico.html', context)


# ============================================================================
# VISTAS PARA EXPORTAR HISTÓRICO - CSV/PDF
# ============================================================================

@login_required(login_url='login')
def exportar_historico_vibraciones_csv(request, cliente_id, sucursal_id):
    """Exportar histórico de vibraciones a CSV"""
    import csv
    from django.http import HttpResponse
    
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    
    # Obtener datos
    activos = Activo.objects.filter(
        equipo__area__sucursal=sucursal,
        activo=True
    ).select_related('equipo', 'equipo__area').order_by(
        'equipo__area__nombre', 'equipo__nombre', 'nombre'
    )
    
    fechas = VibracionesAnalisis.objects.filter(
        activo__equipo__area__sucursal=sucursal
    ).values_list('fecha_muestreo', flat=True).distinct().order_by('-fecha_muestreo')
    
    # Crear respuesta CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="historico_vibraciones_{sucursal.id}_{cliente.id}.csv"'
    
    writer = csv.writer(response, delimiter=',', quoting=csv.QUOTE_ALL)
    
    # Encabezado
    header = ['#', 'Área', 'Equipo', 'Activo']
    for fecha in fechas:
        header.append(f"{fecha.strftime('%d/%m/%Y')}")
    writer.writerow(header)
    
    # Datos
    contador = 1
    for activo in activos:
        fila = [
            contador,
            activo.equipo.area.get_nombre_display(),
            activo.equipo.nombre,
            activo.nombre
        ]
        
        for fecha in fechas:
            try:
                analisis = VibracionesAnalisis.objects.get(
                    activo=activo,
                    fecha_muestreo=fecha
                )
                valor = f"{analisis.get_resultado_display()} ({analisis.velocidad_rms} mm/s)"
                fila.append(valor)
            except VibracionesAnalisis.DoesNotExist:
                fila.append("—")
        
        writer.writerow(fila)
        contador += 1
    
    return response


@login_required(login_url='login')
def exportar_historico_termografias_csv(request, cliente_id, sucursal_id):
    """Exportar histórico de termografías a CSV"""
    import csv
    from django.http import HttpResponse
    
    cliente = get_object_or_404(Cliente, id=cliente_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
    
    # Obtener datos
    activos = Activo.objects.filter(
        equipo__area__sucursal=sucursal,
        activo=True
    ).select_related('equipo', 'equipo__area').order_by(
        'equipo__area__nombre', 'equipo__nombre', 'nombre'
    )
    
    fechas = TermografiaAnalisis.objects.filter(
        activo__equipo__area__sucursal=sucursal
    ).values_list('fecha_muestreo', flat=True).distinct().order_by('-fecha_muestreo')
    
    # Crear respuesta CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="historico_termografias_{sucursal.id}_{cliente.id}.csv"'
    
    writer = csv.writer(response, delimiter=',', quoting=csv.QUOTE_ALL)
    
    # Encabezado
    header = ['#', 'Área', 'Equipo', 'Activo']
    for fecha in fechas:
        header.append(f"{fecha.strftime('%d/%m/%Y')}")
    writer.writerow(header)
    
    # Datos
    contador = 1
    for activo in activos:
        fila = [
            contador,
            activo.equipo.area.get_nombre_display(),
            activo.equipo.nombre,
            activo.nombre
        ]
        
        for fecha in fechas:
            try:
                analisis = TermografiaAnalisis.objects.get(
                    activo=activo,
                    fecha_muestreo=fecha
                )
                valor = f"{analisis.get_resultado_display()} ({analisis.temperatura_maxima}°C)"
                fila.append(valor)
            except TermografiaAnalisis.DoesNotExist:
                fila.append("—")
        
        writer.writerow(fila)
        contador += 1
    
    return response


@login_required(login_url='login')
def exportar_historico_vibraciones_pdf(request, cliente_id, sucursal_id):
    """Exportar histórico de vibraciones a PDF"""
    try:
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        from io import BytesIO
        from datetime import datetime
        
        cliente = get_object_or_404(Cliente, id=cliente_id)
        sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
        
        # Obtener datos
        activos = Activo.objects.filter(
            equipo__area__sucursal=sucursal,
            activo=True
        ).select_related('equipo', 'equipo__area').order_by(
            'equipo__area__nombre', 'equipo__nombre', 'nombre'
        )
        
        fechas = VibracionesAnalisis.objects.filter(
            activo__equipo__area__sucursal=sucursal
        ).values_list('fecha_muestreo', flat=True).distinct().order_by('-fecha_muestreo')
        
        # Crear PDF en memoria
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), topMargin=20, bottomMargin=20)
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#1e5a8e'),
            spaceAfter=12,
            alignment=1
        )
        
        # Contenido
        elements = []
        
        # Título
        title = Paragraph(f"Histórico de Vibraciones - {sucursal.nombre}", title_style)
        elements.append(title)
        
        # Metadata
        metadata = Paragraph(
            f"<b>Cliente:</b> {cliente.nombre} | <b>Generado:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            styles['Normal']
        )
        elements.append(metadata)
        elements.append(Spacer(1, 0.2*inch))
        
        # Datos tabla
        data = [['#', 'Área', 'Equipo', 'Activo']]
        for fecha in fechas:
            data[0].append(fecha.strftime('%d/%m/%Y'))
        
        contador = 1
        for activo in activos:
            fila = [str(contador), 
                   activo.equipo.area.get_nombre_display(),
                   activo.equipo.nombre,
                   activo.nombre]
            
            for fecha in fechas:
                try:
                    analisis = VibracionesAnalisis.objects.get(
                        activo=activo,
                        fecha_muestreo=fecha
                    )
                    valor = f"{analisis.get_resultado_display()}\n{analisis.velocidad_rms} mm/s"
                    fila.append(valor)
                except VibracionesAnalisis.DoesNotExist:
                    fila.append("—")
            
            data.append(fila)
            contador += 1
        
        # Crear tabla
        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e5a8e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
        ]))
        
        elements.append(table)
        
        # Generar PDF
        doc.build(elements)
        
        # Respuesta
        buffer.seek(0)
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="historico_vibraciones_{sucursal.id}.pdf"'
        return response
        
    except ImportError:
        return JsonResponse({
            'error': 'ReportLab no está instalado. Usa CSV en su lugar.'
        }, status=400)


@login_required(login_url='login')
def exportar_historico_termografias_pdf(request, cliente_id, sucursal_id):
    """Exportar histórico de termografías a PDF"""
    try:
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        from io import BytesIO
        from datetime import datetime
        
        cliente = get_object_or_404(Cliente, id=cliente_id)
        sucursal = get_object_or_404(Sucursal, id=sucursal_id, cliente=cliente)
        
        # Obtener datos
        activos = Activo.objects.filter(
            equipo__area__sucursal=sucursal,
            activo=True
        ).select_related('equipo', 'equipo__area').order_by(
            'equipo__area__nombre', 'equipo__nombre', 'nombre'
        )
        
        fechas = TermografiaAnalisis.objects.filter(
            activo__equipo__area__sucursal=sucursal
        ).values_list('fecha_muestreo', flat=True).distinct().order_by('-fecha_muestreo')
        
        # Crear PDF en memoria
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), topMargin=20, bottomMargin=20)
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#c4491e'),
            spaceAfter=12,
            alignment=1
        )
        
        # Contenido
        elements = []
        
        # Título
        title = Paragraph(f"Histórico de Termografías - {sucursal.nombre}", title_style)
        elements.append(title)
        
        # Metadata
        metadata = Paragraph(
            f"<b>Cliente:</b> {cliente.nombre} | <b>Generado:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            styles['Normal']
        )
        elements.append(metadata)
        elements.append(Spacer(1, 0.2*inch))
        
        # Datos tabla
        data = [['#', 'Área', 'Equipo', 'Activo']]
        for fecha in fechas:
            data[0].append(fecha.strftime('%d/%m/%Y'))
        
        contador = 1
        for activo in activos:
            fila = [str(contador), 
                   activo.equipo.area.get_nombre_display(),
                   activo.equipo.nombre,
                   activo.nombre]
            
            for fecha in fechas:
                try:
                    analisis = TermografiaAnalisis.objects.get(
                        activo=activo,
                        fecha_muestreo=fecha
                    )
                    valor = f"{analisis.get_resultado_display()}\n{analisis.temperatura_maxima}°C"
                    fila.append(valor)
                except TermografiaAnalisis.DoesNotExist:
                    fila.append("—")
            
            data.append(fila)
            contador += 1
        
        # Crear tabla
        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#c4491e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
        ]))
        
        elements.append(table)
        
        # Generar PDF
        doc.build(elements)
        
        # Respuesta
        buffer.seek(0)
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="historico_termografias_{sucursal.id}.pdf"'
        return response
        
    except ImportError:
        return JsonResponse({
            'error': 'ReportLab no está instalado. Usa CSV en su lugar.'
        }, status=400)

