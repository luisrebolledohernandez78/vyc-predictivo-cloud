#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

# Cambiar la contraseña del usuario admin
try:
    user = User.objects.get(username='admin')
    user.set_password('VyCingenieria')
    user.save()
    print("✅ Contraseña del usuario 'admin' actualizada exitosamente")
    print("   Usuario: admin")
    print("   Contraseña: VyCingenieria")
except User.DoesNotExist:
    print("❌ El usuario 'admin' no existe")
