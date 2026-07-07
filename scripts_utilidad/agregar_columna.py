"""Agrega la columna fuente a la tabla consultas"""
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database', 'chatbot.db')

print(f"Base de datos: {DB_PATH}")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Ver columnas actuales
cursor.execute("PRAGMA table_info(consultas)")
columnas = [row[1] for row in cursor.fetchall()]
print(f"Columnas actuales: {columnas}")

# Agregar columna fuente si no existe
if 'fuente' not in columnas:
    cursor.execute("ALTER TABLE consultas ADD COLUMN fuente TEXT DEFAULT 'embeddings'")
    conn.commit()
    print("OK: Columna 'fuente' agregada")
else:
    print("INFO: La columna 'fuente' ya existe")

# Verificar
cursor.execute("PRAGMA table_info(consultas)")
print(f"Columnas finales: {[row[1] for row in cursor.fetchall()]}")

conn.close()
print("Listo")
