from django.urls import path
from .views import (
    welcome, user_login, user_logout, dashboard, health,
    vibraciones, crear_cliente_vibraciones, editar_cliente_vibraciones, eliminar_cliente_vibraciones,
    sucursales_vibraciones, crear_sucursal_vibraciones, editar_sucursal_vibraciones, eliminar_sucursal_vibraciones,
    areas_vibraciones, editar_area_vibraciones, eliminar_area_vibraciones,
    termografias, crear_cliente_termografias, editar_cliente_termografias, eliminar_cliente_termografias,
    sucursales_termografias, crear_sucursal_termografias, editar_sucursal_termografias, eliminar_sucursal_termografias,
    areas_termografias, editar_area_termografias, eliminar_area_termografias,
)

urlpatterns = [
    path("", welcome, name="welcome"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("dashboard/", dashboard, name="dashboard"),
    
    # Vibraciones - Clientes
    path("vibraciones/", vibraciones, name="vibraciones"),
    path("vibraciones/cliente/crear/", crear_cliente_vibraciones, name="crear_cliente_vibraciones"),
    path("vibraciones/cliente/<int:cliente_id>/editar/", editar_cliente_vibraciones, name="editar_cliente_vibraciones"),
    path("vibraciones/cliente/<int:cliente_id>/eliminar/", eliminar_cliente_vibraciones, name="eliminar_cliente_vibraciones"),
    
    # Vibraciones - Sucursales
    path("vibraciones/cliente/<int:cliente_id>/sucursales/", sucursales_vibraciones, name="sucursales_vibraciones"),
    path("vibraciones/cliente/<int:cliente_id>/sucursal/crear/", crear_sucursal_vibraciones, name="crear_sucursal_vibraciones"),
    path("vibraciones/cliente/<int:cliente_id>/sucursal/<int:sucursal_id>/editar/", editar_sucursal_vibraciones, name="editar_sucursal_vibraciones"),
    path("vibraciones/cliente/<int:cliente_id>/sucursal/<int:sucursal_id>/eliminar/", eliminar_sucursal_vibraciones, name="eliminar_sucursal_vibraciones"),
    
    # Vibraciones - Áreas
    path("vibraciones/cliente/<int:cliente_id>/sucursal/<int:sucursal_id>/areas/", areas_vibraciones, name="areas_vibraciones"),
    path("vibraciones/cliente/<int:cliente_id>/sucursal/<int:sucursal_id>/area/<int:area_id>/editar/", editar_area_vibraciones, name="editar_area_vibraciones"),
    path("vibraciones/cliente/<int:cliente_id>/sucursal/<int:sucursal_id>/area/<int:area_id>/eliminar/", eliminar_area_vibraciones, name="eliminar_area_vibraciones"),
    
    # Termografías - Clientes
    path("termografias/", termografias, name="termografias"),
    path("termografias/cliente/crear/", crear_cliente_termografias, name="crear_cliente_termografias"),
    path("termografias/cliente/<int:cliente_id>/editar/", editar_cliente_termografias, name="editar_cliente_termografias"),
    path("termografias/cliente/<int:cliente_id>/eliminar/", eliminar_cliente_termografias, name="eliminar_cliente_termografias"),
    
    # Termografías - Sucursales
    path("termografias/cliente/<int:cliente_id>/sucursales/", sucursales_termografias, name="sucursales_termografias"),
    path("termografias/cliente/<int:cliente_id>/sucursal/crear/", crear_sucursal_termografias, name="crear_sucursal_termografias"),
    path("termografias/cliente/<int:cliente_id>/sucursal/<int:sucursal_id>/editar/", editar_sucursal_termografias, name="editar_sucursal_termografias"),
    path("termografias/cliente/<int:cliente_id>/sucursal/<int:sucursal_id>/eliminar/", eliminar_sucursal_termografias, name="eliminar_sucursal_termografias"),
    
    # Termografías - Áreas
    path("termografias/cliente/<int:cliente_id>/sucursal/<int:sucursal_id>/areas/", areas_termografias, name="areas_termografias"),
    path("termografias/cliente/<int:cliente_id>/sucursal/<int:sucursal_id>/area/<int:area_id>/editar/", editar_area_termografias, name="editar_area_termografias"),
    path("termografias/cliente/<int:cliente_id>/sucursal/<int:sucursal_id>/area/<int:area_id>/eliminar/", eliminar_area_termografias, name="eliminar_area_termografias"),
    
    # API
    path("health/", health),
]
