import sqlite3
import os
import hashlib

def get_connection():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DB_PATH = os.path.join(BASE_DIR, 'database', 'chatbot.db')
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Tabla de consultas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT,
            pregunta TEXT NOT NULL,
            intencion TEXT,
            respuesta TEXT,
            fuente TEXT,
            calificacion INTEGER,
            comentario TEXT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de administradores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS administradores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL,
            nombre TEXT,
            email TEXT,
            rol TEXT DEFAULT 'admin',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Crear usuarios SI NO EXISTEN
    usuarios = [
        ('admin', hashlib.sha256('admin123'.encode()).hexdigest(), 'Administrador', 'admin@uniminuto.edu.co', 'admin'),
        ('supervisor', hashlib.sha256('super123'.encode()).hexdigest(), 'Supervisor', 'supervisor@uniminuto.edu.co', 'supervisor'),
    ]
    
    for usuario, contrasena, nombre, email, rol in usuarios:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO administradores (usuario, contrasena, nombre, email, rol)
                VALUES (?, ?, ?, ?, ?)
            ''', (usuario, contrasena, nombre, email, rol))
        except sqlite3.IntegrityError:
            print(f"ℹ️ Usuario {usuario} ya existe")
    
    conn.commit()
    conn.close()
    print("✅ Base de datos inicializada con usuarios admin y supervisor")
    
    # Verificar que los usuarios existen
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT usuario, rol FROM administradores")
    usuarios_existentes = cursor.fetchall()
    print(f"📋 Usuarios en DB: {[dict(u) for u in usuarios_existentes]}")
    conn.close()

if __name__ == '__main__':
    init_db()