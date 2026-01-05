#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

# Crear super usuario si no existe
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@vyc-predictivo.com', 'admin123')
    print("✅ Super usuario 'admin' creado exitosamente")
    print("   Usuario: admin")
    print("   Contraseña: admin123")
    print("   Email: admin@vyc-predictivo.com")
else:
    print("⚠️  El usuario 'admin' ya existe")
