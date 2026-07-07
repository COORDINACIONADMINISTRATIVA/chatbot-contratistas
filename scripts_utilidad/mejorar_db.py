"""Script para mejorar la base de datos"""
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'chatbot.db')
print(f"Base de datos en: {DB_PATH}")

def mejorar_db():
    if not os.path.exists(DB_PATH):
        print(f"ERROR: No existe el archivo {DB_PATH}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Verificar tablas existentes
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tablas = [row[0] for row in cursor.fetchall()]
    print(f"Tablas existentes: {tablas}")
    
    # Agregar columna de feedback
    if 'consultas' in tablas:
        columnas = [row[1] for row in cursor.execute("PRAGMA table_info(consultas)").fetchall()]
        print(f"Columnas actuales de 'consultas': {columnas}")
        
        if 'calificacion' not in columnas:
            cursor.execute("ALTER TABLE consultas ADD COLUMN calificacion INTEGER DEFAULT NULL")
            print("OK: Columna calificacion agregada")
        else:
            print("INFO: calificacion ya existe")
        
        if 'comentario' not in columnas:
            cursor.execute("ALTER TABLE consultas ADD COLUMN comentario TEXT DEFAULT NULL")
            print("OK: Columna comentario agregada")
        else:
            print("INFO: comentario ya existe")
    
    # Crear tabla de administradores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS administradores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL,
            nombre TEXT,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("OK: Tabla administradores lista")
    
    # Crear tabla de logs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs_sistema (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            mensaje TEXT,
            datos TEXT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("OK: Tabla logs_sistema lista")
    
    # Insertar admin
    import hashlib
    contrasena_hash = hashlib.sha256('admin123'.encode()).hexdigest()
    try:
        cursor.execute('''
            INSERT INTO administradores (usuario, contrasena, nombre, email)
            VALUES (?, ?, ?, ?)
        ''', ('admin', contrasena_hash, 'Administrador', 'admin@uniminuto.edu.co'))
        print("OK: Admin creado (usuario: admin, clave: admin123)")
    except sqlite3.IntegrityError:
        print("INFO: Admin ya existe")
    
    conn.commit()
    conn.close()
    print("\nBase de datos mejorada correctamente")

if __name__ == '__main__':
    mejorar_db()
