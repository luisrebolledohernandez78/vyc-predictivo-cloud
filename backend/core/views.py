from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Cliente, Sucursal, Area
from .forms import ClienteForm, SucursalForm, AreaForm


def welcome(request):
    """Página de bienvenida del portal"""
    return render(request, 'core/welcome.html')


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
        'titulo': 'Análisis de Vibraciones',
        'descripcion': 'Monitorea y analiza las vibraciones de tu maquinaria en tiempo real'
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
        'titulo': 'Termografía Infrarroja',
        'descripcion': 'Detecta anomalías térmicas en tu equipamiento industrial'
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
    sucursales = cliente.sucursales.filter(activo=True)
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
    sucursales = cliente.sucursales.filter(activo=True)
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
