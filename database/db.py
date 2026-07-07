import sqlite3
import os

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
            satisfaccion INTEGER,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de intents (intenciones)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS intents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            descripcion TEXT
        )
    ''')
    
    # Tabla de feedback
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            consulta_id INTEGER,
            calificacion INTEGER,
            comentario TEXT,
            FOREIGN KEY (consulta_id) REFERENCES consultas(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Base de datos inicializada")

if __name__ == '__main__':
    init_db()
