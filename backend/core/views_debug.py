#!/usr/bin/env python
"""
Endpoint de prueba para upload sin login (desarrollo)
"""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)

@csrf_exempt  # Desabilitar CSRF solo para este endpoint de debug
@require_http_methods(["POST"])
def test_upload_sin_autenticacion(request, activo_id):
    """
    Endpoint de prueba para debugear uploads SIN @login_required
    SOLO PARA DESARROLLO - No usar en producción
    """
    try:
        logger.info(f"=== TEST UPLOAD SIN AUTH ===")
        logger.info(f"Activo ID: {activo_id}")
        logger.info(f"Request method: {request.method}")
        logger.info(f"FILES: {list(request.FILES.keys())}")
        logger.info(f"META CSRF: {request.META.get('CSRF_COOKIE', 'No cookie')}")
        
        if 'foto' not in request.FILES:
            logger.error("No 'foto' en request.FILES")
            return JsonResponse({'success': False, 'error': 'No archivo'}, status=400)
        
        archivo = request.FILES['foto']
        logger.info(f"Archivo: {archivo.name}, tipo: {archivo.content_type}, size: {archivo.size}")
        
        return JsonResponse({
            'success': True,
            'mensaje': 'Endpoint de prueba',
            'archivo_nombre': archivo.name,
            'archivo_tipo': archivo.content_type,
            'archivo_size': archivo.size
        })
    
    except Exception as e:
        logger.error(f"ERROR EN TEST UPLOAD: {str(e)}", exc_info=True)
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
