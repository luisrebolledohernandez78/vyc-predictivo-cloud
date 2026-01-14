from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Cliente, Sucursal, Area, Equipo, Activo
from .forms import ClienteForm, SucursalForm, AreaForm, EquipoForm, ActivoForm, ExcelUploadForm
from .excel_parser import ExcelEquiposParser
import tempfile


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
        form = SucursalForm(request.POST, instance=sucursal)
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
        form = SucursalForm(request.POST, instance=sucursal)
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
    return render(request, 'core/equipos.html', context)


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
    return render(request, 'core/activos.html', context)


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
    
    if request.method == 'POST':
        form = ActivoForm(request.POST, instance=activo)
        if form.is_valid():
            form.save()
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
        'titulo': f'Editar {activo.nombre}'
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
    activo.delete()
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
    """Página de equipos para una área en termografías"""
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
        'modulo': 'termografias',
        'titulo': f'Equipos - {area.get_nombre_display()}',
        'descripcion': 'Gestiona los equipos y máquinas del área'
    }
    return render(request, 'core/equipos.html', context)


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
    activos = equipo.activos.filter(activo=True).select_related('analisis_termico').order_by('nombre')
    
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
    return render(request, 'core/activos.html', context)


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


@require_http_methods(["POST"])
@login_required
def subir_foto_termica(request, activo_id):
    """Sube una foto térmica para un activo y la analiza automáticamente"""
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        from .models import AnalisisTermico
        
        activo = get_object_or_404(Activo, id=activo_id)
        
        if 'foto' not in request.FILES:
            return JsonResponse({'success': False, 'error': 'No se proporcionó archivo'}, status=400)
        
        archivo = request.FILES['foto']
        logger.info(f"Archivo recibido: {archivo.name}, tipo: {archivo.content_type}, tamaño: {archivo.size}")
        
        # Validar que sea una imagen
        if not archivo.content_type.startswith('image/'):
            return JsonResponse({'success': False, 'error': 'El archivo debe ser una imagen'}, status=400)
        
        # Eliminar foto anterior si existe
        if activo.foto_termica:
            activo.foto_termica.delete()
        
        # Guardar nueva foto
        activo.foto_termica = archivo
        activo.save()
        logger.info(f"✅ Foto guardada correctamente")
        
        # Intentar analizar - si falla, devolvemos la foto sin análisis
        resultado_analisis = None
        try:
            from .analisis_termico import AnalizadorTermico
            analizador = AnalizadorTermico()
            logger.info(f"🔬 Iniciando análisis OCR...")
            resultado_analisis = analizador.analizar_imagen(activo.foto_termica)
            logger.info(f"📊 Resultado análisis: {resultado_analisis}")
        except Exception as ocr_error:
            logger.warning(f"⚠️ OCR no disponible: {str(ocr_error)}")
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
        
        # Guardar o actualizar análisis
        analisis, creado = AnalisisTermico.objects.update_or_create(
            activo=activo,
            defaults={
                'temperatura_promedio': resultado_analisis['temperatura_promedio'],
                'temperatura_maxima': resultado_analisis['temperatura_maxima'],
                'temperatura_minima': resultado_analisis['temperatura_minima'],
                'rango_minimo': resultado_analisis['rango_minimo'],
                'rango_maximo': resultado_analisis['rango_maximo'],
                'porcentaje_zona_critica': resultado_analisis['porcentaje_zona_critica'],
                'porcentaje_zona_alerta': resultado_analisis['porcentaje_zona_alerta'],
                'estado': resultado_analisis['estado'],
            }
        )
        logger.info(f"✅ Análisis {'creado' if creado else 'actualizado'} para activo {activo_id}")
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


@require_http_methods(["GET"])
@login_required(login_url='/login/')
def obtener_analisis_termico(request, activo_id):
    """Obtiene el análisis térmico guardado para un activo"""
    try:
        from .models import AnalisisTermico
        import logging
        
        logger = logging.getLogger(__name__)
        
        activo = get_object_or_404(Activo, id=activo_id)
        
        # Intentar obtener el análisis guardado usando el related_name correcto
        if not hasattr(activo, 'analisis_termico') or activo.analisis_termico is None:
            logger.warning(f"No existe análisis para activo {activo_id}")
            return JsonResponse({
                'success': False,
                'error': 'No hay análisis disponible para este activo'
            }, status=404)
        
        analisis = activo.analisis_termico
        
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


@api_view(["GET"])
def health(request):
    return Response({"status": "ok", "service": "vyc-predictivo-cloud"})

