from django.urls import path
from .views import (
    welcome, user_login, user_logout, dashboard, health,
    vibraciones, crear_cliente_vibraciones, editar_cliente_vibraciones, eliminar_cliente_vibraciones,
    sucursales_vibraciones, crear_sucursal_vibraciones, editar_sucursal_vibraciones, eliminar_sucursal_vibraciones,
    areas_vibraciones, editar_area_vibraciones, eliminar_area_vibraciones,
    equipos_vibraciones, crear_equipo_vibraciones, editar_equipo_vibraciones, eliminar_equipo_vibraciones,
    activos_vibraciones, crear_activo_vibraciones, editar_activo_vibraciones, eliminar_activo_vibraciones,
    upload_equipos_vibraciones, confirmar_upload_equipos_vibraciones,
    termografias, crear_cliente_termografias, editar_cliente_termografias, eliminar_cliente_termografias,
    sucursales_termografias, crear_sucursal_termografias, editar_sucursal_termografias, eliminar_sucursal_termografias,
    areas_termografias, editar_area_termografias, eliminar_area_termografias,
    equipos_termografias, crear_equipo_termografias, editar_equipo_termografias, eliminar_equipo_termografias,
    activos_termografias, crear_activo_termografias, editar_activo_termografias, eliminar_activo_termografias,
    upload_equipos_termografias, confirmar_upload_equipos_termografias,
    actualizar_estado_equipo, actualizar_observacion_equipo, actualizar_estado_activo, actualizar_observacion_activo,
    subir_foto_termica, configuracion, upload_profile_photo, save_config,
)
from .views_debug import test_upload_sin_autenticacion

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
    
    # Vibraciones - Equipos
    path("vibraciones/cliente/<int:cliente_id>/sucursal/<int:sucursal_id>/area/<int:area_id>/equipos/", equipos_vibraciones, name="equipos_vibraciones"),
    path("vibraciones/cliente/<int:cliente_id>/sucursal/<int:sucursal_id>/area/<int:area_id>/equipo/crear/", crear_equipo_vibraciones, name="crear_equipo_vibraciones"),
    path("vibraciones/cliente/<int:cliente_id>/sucursal/<int:sucursal_id>/area/<int:area_id>/equipo/<int:equipo_id>/editar/", editar_equipo_vibraciones, name="editar_equipo_vibraciones"),
    path("vibraciones/cliente/<int:cliente_id>/sucursal/<int:sucursal_id>/area/<int:area_id>/equipo/<int:equipo_id>/eliminar/", eliminar_equipo_vibraciones, name="eliminar_equipo_vibraciones"),
    
    # Vibraciones - Activos
    path("vibraciones/cliente/<int:cliente_id>/sucursal/<int:sucursal_id>/area/<int:area_id>/equipo/<int:equipo_id>/activos/", activos_vibraciones, name="activos_vibraciones"),
    path("vibraciones/cliente/<int:cliente_id>/sucursal/<int:sucursal_id>/area/<int:area_id>/equipo/<int:equipo_id>/activo/crear/", crear_activo_vibraciones, name="crear_activo_vibraciones"),
    path("vibraciones/cliente/<int:cliente_id>/sucursal/<int:sucursal_id>/area/<int:area_id>/equipo/<int:equipo_id>/activo/<int:activo_id>/editar/", editar_activo_vibraciones, name="editar_activo_vibraciones"),
    path("vibraciones/cliente/<int:cliente_id>/sucursal/<int:sucursal_id>/area/<int:area_id>/equipo/<int:equipo_id>/activo/<int:activo_id>/eliminar/", eliminar_activo_vibraciones, name="eliminar_activo_vibraciones"),
    
    # Vibraciones - Upload Excel
    path("vibraciones/cliente/<int:cliente_id>/sucursal/<int:sucursal_id>/upload-equipos/", upload_equipos_vibraciones, name="upload_equipos_vibraciones"),
    path("vibraciones/cliente/<int:cliente_id>/sucursal/<int:sucursal_id>/confirmar-upload/", confirmar_upload_equipos_vibraciones, name="confirmar_upload_equipos_vibraciones"),
    
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
    
    # Termografías - Equipos
    path("termografias/cliente/<int:cliente_id>/sucursal/<int:sucursal_id>/area/<int:area_id>/equipos/", equipos_termografias, name="equipos_termografias"),
    path("termografias/cliente/<int:cliente_id>/sucursal/<int:sucursal_id>/area/<int:area_id>/equipo/crear/", crear_equipo_termografias, name="crear_equipo_termografias"),
    path("termografias/cliente/<int:cliente_id>/sucursal/<int:sucursal_id>/area/<int:area_id>/equipo/<int:equipo_id>/editar/", editar_equipo_termografias, name="editar_equipo_termografias"),
    path("termografias/cliente/<int:cliente_id>/sucursal/<int:sucursal_id>/area/<int:area_id>/equipo/<int:equipo_id>/eliminar/", eliminar_equipo_termografias, name="eliminar_equipo_termografias"),
    
    # Termografías - Activos
    path("termografias/cliente/<int:cliente_id>/sucursal/<int:sucursal_id>/area/<int:area_id>/equipo/<int:equipo_id>/activos/", activos_termografias, name="activos_termografias"),
    path("termografias/cliente/<int:cliente_id>/sucursal/<int:sucursal_id>/area/<int:area_id>/equipo/<int:equipo_id>/activo/crear/", crear_activo_termografias, name="crear_activo_termografias"),
    path("termografias/cliente/<int:cliente_id>/sucursal/<int:sucursal_id>/area/<int:area_id>/equipo/<int:equipo_id>/activo/<int:activo_id>/editar/", editar_activo_termografias, name="editar_activo_termografias"),
    path("termografias/cliente/<int:cliente_id>/sucursal/<int:sucursal_id>/area/<int:area_id>/equipo/<int:equipo_id>/activo/<int:activo_id>/eliminar/", eliminar_activo_termografias, name="eliminar_activo_termografias"),
    
    # Termografías - Upload Excel
    path("termografias/cliente/<int:cliente_id>/sucursal/<int:sucursal_id>/upload-equipos/", upload_equipos_termografias, name="upload_equipos_termografias"),
    path("termografias/cliente/<int:cliente_id>/sucursal/<int:sucursal_id>/confirmar-upload/", confirmar_upload_equipos_termografias, name="confirmar_upload_equipos_termografias"),
    
    # API
    path("api/equipo/<int:equipo_id>/actualizar-estado/", actualizar_estado_equipo, name="actualizar_estado_equipo"),
    path("api/equipo/<int:equipo_id>/actualizar-observacion/", actualizar_observacion_equipo, name="actualizar_observacion_equipo"),
    path("api/activo/<int:activo_id>/actualizar-estado/", actualizar_estado_activo, name="actualizar_estado_activo"),
    path("api/activo/<int:activo_id>/actualizar-observacion/", actualizar_observacion_activo, name="actualizar_observacion_activo"),
    path("api/activo/<int:activo_id>/subir-foto-termica/", subir_foto_termica, name="subir_foto_termica"),
    
    # DEBUG: Endpoint de prueba sin autenticación
    path("api/debug/activo/<int:activo_id>/test-upload/", test_upload_sin_autenticacion, name="test_upload_debug"),
    
    # Configuración
    path("configuracion/", configuracion, name="configuracion"),
    path("api/upload-profile-photo/", upload_profile_photo, name="upload_profile_photo"),
    path("api/save-config/", save_config, name="save_config"),
    
    path("health/", health),
]
