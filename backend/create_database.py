#!/usr/bin/env python
import MySQLdb

# Conexión a MySQL sin especificar base de datos
connection = MySQLdb.connect(
    host='127.0.0.1',
    user='root',
    passwd='VyCingenieria',
    port=3306,
)

cursor = connection.cursor()

try:
    # Crear la base de datos
    cursor.execute("CREATE DATABASE IF NOT EXISTS vyc_predictivo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    print("✅ Base de datos 'vyc_predictivo' creada o ya existe")
    connection.commit()
except Exception as e:
    print(f"❌ Error al crear la base de datos: {e}")
finally:
    cursor.close()
    connection.close()
