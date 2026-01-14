#!/usr/bin/env python
"""
Script para probar upload de foto térmica directamente en Django
Sin necesidad de HTTP/requests
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, 's:\\vyc-predictivo-cloud\\backend')

django.setup()

from django.core.files.uploadedfile import SimpleUploadedFile
from core.models import Activo, AnalisisTermico
from core.analisis_termico import AnalizadorTermico
from pathlib import Path

print("🧪 Test de Upload de Foto Térmica (Django ORM)")
print("=" * 60)

# Verificar que existe la imagen de prueba
imagen_path = Path('imagen_termica_prueba.jpg')
if not imagen_path.exists():
    print(f"❌ No se encontró: {imagen_path}")
    sys.exit(1)

print(f"✅ Imagen encontrada: {imagen_path}")
print(f"   Tamaño: {imagen_path.stat().st_size} bytes")

# Buscar un activo
print("\n🔍 Buscando activos...")
activos = Activo.objects.all()[:5]
if not activos:
    print("❌ No hay activos en la BD")
    sys.exit(1)

print(f"✅ Encontrados {len(activos)} activos")
for activo in activos:
    print(f"   - ID {activo.id}: {activo.nombre}")

# Usar el primer activo
activo = activos[0]
print(f"\n📌 Usando activo: {activo.nombre} (ID: {activo.id})")

# Simular upload de archivo
print("\n📤 Subiendo foto...")
with open(imagen_path, 'rb') as f:
    contenido = f.read()

archivo_upload = SimpleUploadedFile(
    name='foto_termica_prueba.jpg',
    content=contenido,
    content_type='image/jpeg'
)

# Guardar foto
print("   Guardando en modelo...")
activo.foto_termica = archivo_upload
activo.save()
print(f"   ✅ Foto guardada en: {activo.foto_termica.path if hasattr(activo.foto_termica, 'path') else activo.foto_termica.name}")

# Analizar
print("\n🔬 Analizando imagen térmica...")
analizador = AnalizadorTermico()
resultado = analizador.analizar_imagen(activo.foto_termica)

if 'error' in resultado:
    print(f"   ❌ Error: {resultado['error']}")
    sys.exit(1)

print("   ✅ Análisis exitoso")

# Guardar análisis en BD
print("\n💾 Guardando análisis en base de datos...")
analisis, creado = AnalisisTermico.objects.update_or_create(
    activo=activo,
    defaults={
        'temperatura_promedio': resultado['temperatura_promedio'],
        'temperatura_maxima': resultado['temperatura_maxima'],
        'temperatura_minima': resultado['temperatura_minima'],
        'porcentaje_zona_critica': resultado['porcentaje_zona_critica'],
        'porcentaje_zona_alerta': resultado['porcentaje_zona_alerta'],
        'estado': resultado['estado'],
    }
)
print(f"   {'✅ Creado' if creado else '✅ Actualizado'}: AnalisisTermico para {activo.nombre}")

# Mostrar resultados
print("\n" + "=" * 60)
print("📊 RESULTADOS DEL ANÁLISIS")
print("=" * 60)
print(f"Estado: {resultado['estado'].upper()}")
print(f"Mensaje: {resultado['mensaje']}")
print(f"\n🌡️ Temperaturas:")
print(f"   Promedio:  {resultado['temperatura_promedio']:.2f}°C")
print(f"   Máxima:    {resultado['temperatura_maxima']:.2f}°C")
print(f"   Mínima:    {resultado['temperatura_minima']:.2f}°C")
print(f"\n📈 Zonas:")
print(f"   Zona Crítica:    {resultado['porcentaje_zona_critica']:.2f}%")
print(f"   Zona Alerta:     {resultado['porcentaje_zona_alerta']:.2f}%")
print(f"   Zona Caliente:   {resultado['porcentaje_zona_caliente']:.2f}%")

print("\n✅ Todo funcionó correctamente!")
print(f"\n💡 El problema en el navegador probablemente es:")
print(f"   1. CSRF token inválido o expirado")
print(f"   2. No está pasando el csrfmiddlewaretoken en la petición")
print(f"   3. La sesión no está manteniendo login")
