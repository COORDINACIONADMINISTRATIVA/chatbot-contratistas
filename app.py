"""
Chatbot de Contratación - API Completa
Arquitectura: Embeddings (Sentence-BERT) + IA Generativa (Llama 3.1) + Excel
Versión corregida - imports al inicio
"""
import os
import sys
import uuid
import hashlib
import time
from datetime import datetime, timedelta
from functools import wraps
from collections import Counter
from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
import pandas as pd
from contratacion.lector_seguimiento import lector_seguimiento

# ==================== IMPORTS AL INICIO ====================
# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Imports del proyecto
from database.db import get_connection, init_db
from contratacion.chatbot_contratista import responder_contratista
from contratacion.lector import lector
from contratacion.intérprete import traducir_observacion, traducir_estado

# ==================== CONFIGURACIÓN ====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')
STATIC_DIR = os.path.join(FRONTEND_DIR, 'static')

app = Flask(__name__, static_folder=STATIC_DIR, static_url_path='/static')
app.secret_key = 'clave-secreta-cambiala-2026-jhfjdsfkjdshfkjsdhfkj'

# Configuración de sesiones
app.permanent_session_lifetime = timedelta(hours=8)
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_DOMAIN'] = None

CORS(app, supports_credentials=True)

print(f"Frontend sirviendo desde: {FRONTEND_DIR}")
print(f"Estáticos sirviendo desde: {STATIC_DIR}")
print(f"CSS existe: {os.path.exists(os.path.join(STATIC_DIR, 'css', 'estilos.css'))}")

# Inicializar base de datos
init_db()


# ==================== RUTAS DE PÁGINAS ====================

@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/consultas')
def consultas():
    return send_from_directory(FRONTEND_DIR, 'consultas.html')


@app.route('/buscar')
def buscar():
    return send_from_directory(FRONTEND_DIR, 'buscar.html')


@app.route('/login')
def login_page():
    return send_from_directory(FRONTEND_DIR, 'login.html')


@app.route('/admin')
def admin():
    return send_from_directory(FRONTEND_DIR, 'admin.html')


@app.route('/supervisor')
def supervisor_page():
    return send_from_directory(FRONTEND_DIR, 'supervisor.html')


# ==================== API CHAT ====================

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    pregunta = data.get('mensaje', '').strip()
    usuario = data.get('usuario', f'anonimo_{uuid.uuid4().hex[:8]}')

    if not pregunta:
        return jsonify({'error': 'Mensaje vacio'}), 400

    respuesta = responder_contratista(pregunta)
    intencion = 'contratista'
    confianza = 1.0
    fuente = 'contratista_excel'

    consulta_id = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO consultas (usuario, pregunta, intencion, respuesta, fuente)
                VALUES (?, ?, ?, ?, ?)
            ''', (usuario, pregunta, intencion, respuesta, fuente))
        except:
            cursor.execute('''
                INSERT INTO consultas (usuario, pregunta, intencion, respuesta)
                VALUES (?, ?, ?, ?)
            ''', (usuario, pregunta, intencion, respuesta))
        consulta_id = cursor.lastrowid
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error guardando: {e}")

    return jsonify({
        'consulta_id': consulta_id,
        'respuesta': respuesta,
        'intencion': intencion,
        'confianza': confianza,
        'fuente': fuente,
        'requiere_humano': False,
        'timestamp': datetime.now().isoformat()
    })


# ==================== API CONTRATISTAS (CRUDO) ====================

@app.route('/api/contratista', methods=['POST'])
def consultar_contratista_api():
    data = request.get_json()
    cedula = data.get('cedula', '').strip()
    nombre = data.get('nombre', '').strip()
    
    if not cedula and not nombre:
        return jsonify({'error': 'Necesito cédula o nombre'}), 400
    
    try:
        if cedula:
            resultados = lector.buscar_por_cedula(cedula)
        elif nombre:
            resultados = lector.buscar_por_nombre(nombre)
        
        if not resultados:
            return jsonify({
                'encontrado': False,
                'mensaje': 'No encontré contratista con esos datos.'
            })
        
        contratistas = []
        for r in resultados:
            contratistas.append({
                'nombre': r.get('NOMBRE DE CONTRATISTA', 'Sin nombre'),
                'cedula': r.get('CEDULA', ''),
                'estado': r.get('ESTADO', 'Sin estado'),
                'observacion': r.get('OBSERVACIÓN', 'Sin observaciones'),
                'año': str(r.get('AÑO', '')),
            })
        
        return jsonify({
            'encontrado': True,
            'cantidad': len(contratistas),
            'contratistas': contratistas
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== API MI PROCESO (TRADUCIDO) ====================

@app.route('/api/mi-proceso', methods=['POST'])
def mi_proceso():
    """Devuelve el estado del contratista con observaciones y pagos"""
    data = request.get_json()
    cedula = data.get('cedula', '').strip()
    
    if not cedula:
        return jsonify({'error': 'Necesito la cédula'}), 400
    
    try:
        # 1. Buscar en Excel de contratistas (resumen)
        registros = lector.buscar_por_cedula(cedula)
        
        # 2. Buscar en Excel de seguimiento (detalle de pagos)
        seguimiento = lector_seguimiento.buscar_por_cedula(cedula)
        
        contratistas = []
        
        # 3. Si hay registros del resumen, agregarlos
        if registros:
            for r in registros:
                # Traducir estado
                estado_original = r.get('ESTADO', 'Sin estado')
                estado_traducido = traducir_estado(estado_original)
                if not estado_traducido:
                    estado_traducido = f"📋 {estado_original}"
                
                # Traducir observación
                obs_original = r.get('OBSERVACIÓN', '')
                obs_traducida = traducir_observacion(obs_original)
                if not obs_traducida or len(obs_traducida) < 10:
                    if obs_original and str(obs_original).lower() not in ['nan', 'none', '']:
                        obs_traducida = f"📋 {obs_original}"
                    else:
                        obs_traducida = "📋 Sin información adicional"
                
                contratistas.append({
                    'nombre': r.get('NOMBRE DE CONTRATISTA', 'Sin nombre'),
                    'cedula': r.get('CEDULA', cedula),
                    'estado': estado_traducido,
                    'observacion': obs_traducida,
                    'año': str(r.get('AÑO', '')),
                    'tipo': 'resumen'
                })
        
        # 4. Si hay registros de seguimiento, agrupar por SOLPEDIDO
        if seguimiento:
            solpedidos = {}
            for s in seguimiento:
                solpedido = str(s.get('N SOLPEDIDO', 'Desconocido'))
                if solpedido not in solpedidos:
                    solpedidos[solpedido] = {
                        'solpedido': solpedido,
                        'nombre': s.get('NOMBRE DE CONTRATISTA', 'Sin nombre'),
                        'cedula': s.get('CEDULA', cedula),
                        'pagos': []
                    }
                
                # Extraer info del POS
                info_pos = lector_seguimiento.extraer_info_pos(s.get('OBJETO DEL CONTRATO', ''))
                
                estado = s.get('ESTADO', 'Sin estado')
                
                solpedidos[solpedido]['pagos'].append({
                    'pos': str(s.get('POS', '')),
                    'estado': estado,
                    'observacion': s.get('OBSERVACIÓN', 'Sin observaciones'),
                    'tipo_pago': info_pos.get('tipo_pago', 'Pago'),
                    'mes': info_pos.get('mes', ''),
                    'valor': s.get('VALOR_DEL_CONTRATO', 0),
                    'es_eliminado': 'Eliminado' in str(estado) or 'ELIMINADO' in str(estado).upper()
                })
            
            # Agregar a la respuesta
            for solpedido, data_s in solpedidos.items():
                contratistas.append({
                    'nombre': data_s['nombre'],
                    'cedula': data_s['cedula'],
                    'solpedido': solpedido,
                    'pagos': data_s['pagos'],
                    'total_pagos': len(data_s['pagos']),
                    'tipo': 'seguimiento'
                })
        
        if not contratistas:
            return jsonify({
                'encontrado': False,
                'mensaje': f'No encontré información con la cédula {cedula}. Verifica que esté bien escrita.'
            })
        
        return jsonify({
            'encontrado': True,
            'cantidad': len(contratistas),
            'contratistas': contratistas
        })
        
    except Exception as e:
        import traceback
        print("ERROR en mi-proceso:", e)
        traceback.print_exc()
        return jsonify({
            'encontrado': False,
            'mensaje': f'Error al procesar: {str(e)}',
            'error_tecnico': str(e)
        }), 500

# ==================== API FEEDBACK ====================

@app.route('/api/feedback', methods=['POST'])
def feedback():
    data = request.get_json()
    consulta_id = data.get('consulta_id')
    calificacion = data.get('calificacion')
    comentario = data.get('comentario', '')

    if not consulta_id or not calificacion:
        return jsonify({'error': 'Datos incompletos'}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE consultas SET calificacion = ?, comentario = ? WHERE id = ?
        ''', (calificacion, comentario, consulta_id))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== SUBIR Y VALIDAR RUT ====================

@app.route('/api/validar-rut', methods=['POST'])
def validar_rut():
    """Recibe un RUT en PDF, lo valida y devuelve el resultado"""
    from werkzeug.utils import secure_filename
    from contratacion.validador_rut import validar_rut_archivo    
    
    # Detectar nombre del campo
    archivo = None
    for key in ['archivo', 'rut', 'file']:
        if key in request.files:
            archivo = request.files[key]
            break
    
    if archivo is None or archivo.filename == '':
        return jsonify({
            'success': False,
            'error': 'No se envió ningún archivo. Selecciona tu RUT en PDF.'
        }), 400
    
    if not archivo.filename.lower().endswith('.pdf'):
        return jsonify({
            'success': False,
            'error': 'Solo se aceptan archivos PDF.'
        }), 400
    
    cedula = request.form.get('cedula', '').strip()
    
    # Obtener info del contratista si hay cédula
    contratista_info = None
    if cedula:
        try:
            registros = lector.buscar_por_cedula(cedula)
            if registros:
                contratista_info = lector.obtener_info_contratista(registros[0])
        except:
            pass
    
    # Guardar archivo temporalmente
    UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    nombre_seguro = secure_filename(archivo.filename)
    ruta_archivo = os.path.join(UPLOAD_DIR, nombre_seguro)
    archivo.save(ruta_archivo)
    
    try:
        # Analizar RUT (devuelve el texto legible y el dict con los datos)
        respuesta, resultado = validar_rut_archivo(ruta_archivo, cedula)
        
        # Agregar info del contratista a los datos extraídos
        if contratista_info:
            resultado['datos_extraidos']['nombre_contratista'] = contratista_info.get('nombre')
            resultado['datos_extraidos']['cedula_contratista'] = contratista_info.get('cedula')
        
        # Limpiar
        try:
            os.remove(ruta_archivo)
        except:
            pass
        
        return jsonify({
            'success': True,
            'valido': resultado['valido'],
            'datos': resultado['datos_extraidos'],
            'errores': resultado['errores'],
            'advertencias': resultado['advertencias'],
            'exitos': resultado['exitos'],
            'respuesta': respuesta,
            'archivo_procesado': archivo.filename
        })
    except Exception as e:
        try:
            os.remove(ruta_archivo)
        except:
            pass
        return jsonify({
            'success': False,
            'error': f'Error al procesar el RUT: {str(e)}'
        }), 500


# ==================== ADMINISTRACIÓN ====================

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'admin_id' not in session:
            return jsonify({'error': 'No autorizado'}), 401
        return f(*args, **kwargs)
    return decorated


@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    if not request.is_json:
        return jsonify({'success': False, 'error': 'Se requiere JSON'}), 400
    
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'No se recibieron datos'}), 400
    
    usuario = data.get('usuario')
    contrasena = data.get('contrasena')
    
    if not usuario or not contrasena:
        return jsonify({'success': False, 'error': 'Faltan usuario o contraseña'}), 400
    
    contrasena_hash = hashlib.sha256(contrasena.encode()).hexdigest()
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM administradores WHERE usuario = ? AND contrasena = ?',
            (usuario, contrasena_hash)
        )
        admin = cursor.fetchone()
        conn.close()
        
        if not admin:
            return jsonify({'success': False, 'error': 'Credenciales inválidas'}), 401
        
        session.permanent = True
        session['admin_id'] = admin['id']
        session['admin_usuario'] = admin['usuario']
        session['admin_nombre'] = admin['nombre']
        session['admin_rol'] = 'supervisor' if admin['usuario'] == 'supervisor' else 'admin'
        
        return jsonify({
            'success': True,
            'admin': {
                'id': admin['id'],
                'usuario': admin['usuario'],
                'nombre': admin['nombre'],
                'rol': session['admin_rol']
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/logout', methods=['POST'])
@admin_required
def admin_logout():
    session.clear()
    return jsonify({'success': True})


# ==================== ESTADÍSTICAS ADMIN ====================

@app.route('/api/admin/estadisticas-contratistas', methods=['GET'])
@admin_required
def estadisticas_contratistas():
    import re
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) as total FROM consultas')
        total = cursor.fetchone()['total']
        cursor.execute("SELECT COUNT(*) as total FROM consultas WHERE DATE(fecha) = DATE('now')")
        hoy = cursor.fetchone()['total']
        cursor.execute('SELECT COUNT(DISTINCT usuario) as unicos FROM consultas')
        usuarios_unicos = cursor.fetchone()['unicos']
        cursor.execute("SELECT COUNT(*) as total FROM consultas WHERE pregunta GLOB '[0-9][0-9][0-9][0-9][0-9][0-9]*'")
        cedulas_consultadas = cursor.fetchone()['total']
        cursor.execute("SELECT AVG(calificacion) as promedio, COUNT(calificacion) as total_cal, SUM(CASE WHEN calificacion >= 4 THEN 1 ELSE 0 END) as positivas, SUM(CASE WHEN calificacion <= 2 THEN 1 ELSE 0 END) as negativas FROM consultas WHERE calificacion IS NOT NULL")
        sat = cursor.fetchone()
        cursor.execute("SELECT calificacion, COUNT(*) as cantidad FROM consultas WHERE calificacion IS NOT NULL GROUP BY calificacion ORDER BY calificacion")
        dist = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for r in cursor.fetchall():
            dist[r['calificacion']] = r['cantidad']
        distribucion_satisfaccion = [dist[1], dist[2], dist[3], dist[4], dist[5]]
        cursor.execute("SELECT DATE(fecha) as dia, COUNT(*) as cantidad FROM consultas WHERE fecha >= DATE('now', '-7 days') GROUP BY DATE(fecha) ORDER BY dia")
        por_dia = [dict(row) for row in cursor.fetchall()]

        categorias = {'documentos': 0, 'portal': 0, 'rut': 0, 'pagos': 0, 'problemas': 0, 'llenar': 0}
        cursor.execute('SELECT pregunta FROM consultas')
        todas_preguntas = cursor.fetchall()
        for row in todas_preguntas:
            pregunta = (row['pregunta'] or '').lower()
            if re.search(r'\b\d{6,12}\b', pregunta):
                categorias['portal'] += 1
            if any(p in pregunta for p in ['documento', 'papel', 'qué necesito']):
                categorias['documentos'] += 1
            if any(p in pregunta for p in ['portal', 'plataforma', 'registro', 'registrarme']):
                categorias['portal'] += 1
            if 'rut' in pregunta:
                categorias['rut'] += 1
            if any(p in pregunta for p in ['pago', 'factura', 'dinero', 'plata']):
                categorias['pagos'] += 1
            if any(p in pregunta for p in ['problema', 'error', 'no puedo', 'rechazo']):
                categorias['problemas'] += 1
            if any(p in pregunta for p in ['llenar', 'campo', 'cómo lleno']):
                categorias['llenar'] += 1

        conn.close()
        return jsonify({
            'total_consultas': total, 'consultas_hoy': hoy, 'usuarios_unicos': usuarios_unicos,
            'cedulas_consultadas': cedulas_consultadas,
            'satisfaccion_promedio': round(float(sat['promedio'] or 0), 2),
            'total_calificadas': sat['total_cal'],
            'satisfaccion_positiva': sat['positivas'] or 0,
            'satisfaccion_negativa': sat['negativas'] or 0,
            'distribucion_satisfaccion': distribucion_satisfaccion,
            'consultas_por_dia': por_dia, 'categorias': categorias
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/consultas', methods=['GET'])
@admin_required
def listar_consultas():
    limite = request.args.get('limite', 50, type=int)
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM consultas ORDER BY fecha DESC LIMIT ?', (limite,))
        consultas = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify({'consultas': consultas, 'total': len(consultas)})
    except Exception as e:
        return jsonify({'error': str(e), 'consultas': []}), 500


# ==================== ENDPOINT DEL SUPERVISOR (ARREGLADO USANDO EXCEL) ====================

@app.route('/api/supervisor/dashboard', methods=['GET'])
@admin_required
def supervisor_dashboard():
    import traceback
    try:
        # Usar el DataFrame del lector para obtener estadísticas
        df = lector.df
        if df is None or df.empty:
            return jsonify({
                'total_contratistas_unicos': 0,
                'total_contratos': 0,
                'promedio_contratos': 0,
                'chat': {'total_consultas': 0, 'usuarios_unicos': 0, 'cedulas_consultadas': 0, 'categorias': {}, 'ultimas_consultas': [], 'positivas': 0, 'negativas': 0},
                'estados': {'labels': [], 'values': []},
                'tipos_problemas': {},
                'por_anio': {},
                'top_problemas': [],
                'sin_movimiento': [],
                'contratistas': []
            })

        # Estadísticas de contratos
        total_contratos = len(df)
        cedulas_unicas = df['CEDULA'].nunique() if 'CEDULA' in df.columns else 0
        promedio = round(total_contratos / cedulas_unicas, 2) if cedulas_unicas > 0 else 0

        # Estados (top 10)
        if 'ESTADO' in df.columns:
            estados_counts = df['ESTADO'].value_counts().head(10)
            estados_data = {
                'labels': estados_counts.index.tolist(),
                'values': estados_counts.values.tolist()
            }
        else:
            estados_data = {'labels': [], 'values': []}

        # Años
        if 'AÑO' in df.columns:
            anios_counts = df['AÑO'].value_counts()
            por_anio = {str(k): v for k, v in anios_counts.items() if pd.notna(k)}
        else:
            por_anio = {}

        # Observaciones y problemas (simplificado)
        tipos_problemas = {}
        if 'OBSERVACIÓN' in df.columns:
            for obs in df['OBSERVACIÓN'].dropna():
                obs_upper = str(obs).upper()
                if 'RECHAZ' in obs_upper:
                    tipos_problemas['Rechazo'] = tipos_problemas.get('Rechazo', 0) + 1
                if 'NO CONTESTA' in obs_upper:
                    tipos_problemas['No contesta'] = tipos_problemas.get('No contesta', 0) + 1
                if 'RUT' in obs_upper and ('MAL' in obs_upper or 'CORRECCION' in obs_upper):
                    tipos_problemas['RUT'] = tipos_problemas.get('RUT', 0) + 1
                if 'REGIMEN' in obs_upper:
                    tipos_problemas['Régimen'] = tipos_problemas.get('Régimen', 0) + 1
                if 'SEDE' in obs_upper:
                    tipos_problemas['Sede'] = tipos_problemas.get('Sede', 0) + 1
                if 'DOCUMENTOS' in obs_upper:
                    tipos_problemas['Documentos'] = tipos_problemas.get('Documentos', 0) + 1
                if 'CONTRASEÑA' in obs_upper or 'CLAVE' in obs_upper:
                    tipos_problemas['Con clave'] = tipos_problemas.get('Con clave', 0) + 1

        # Top contratistas con más problemas (basado en observaciones)
        top_problemas = []
        if 'CEDULA' in df.columns and 'OBSERVACIÓN' in df.columns:
            grouped = df.groupby('CEDULA').agg({
                'NOMBRE DE CONTRATISTA': 'first',
                'OBSERVACIÓN': lambda x: x.count(),
                'ESTADO': 'count'
            }).reset_index()
            grouped.columns = ['cedula', 'nombre', 'total_problemas', 'total_contratos']
            grouped = grouped[grouped['total_problemas'] > 0].sort_values('total_problemas', ascending=False).head(15)
            top_problemas = grouped.to_dict('records')

        # Datos del chat (desde SQLite)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) as total FROM consultas')
        total_chat = cursor.fetchone()['total']
        cursor.execute('SELECT COUNT(DISTINCT usuario) as unicos FROM consultas')
        usuarios_unicos = cursor.fetchone()['unicos']
        cursor.execute("SELECT COUNT(*) as total FROM consultas WHERE pregunta GLOB '[0-9][0-9][0-9][0-9][0-9][0-9]*'")
        cedulas_consultadas = cursor.fetchone()['total']
        cursor.execute('SELECT * FROM consultas ORDER BY fecha DESC LIMIT 50')
        ultimas_consultas = [dict(row) for row in cursor.fetchall()]
        cursor.execute("SELECT COUNT(*) FROM consultas WHERE calificacion >= 4")
        positivas = cursor.fetchone()[0] or 0
        cursor.execute("SELECT COUNT(*) FROM consultas WHERE calificacion <= 2")
        negativas = cursor.fetchone()[0] or 0
        conn.close()

        chat_data = {
            'total_consultas': total_chat,
            'usuarios_unicos': usuarios_unicos,
            'cedulas_consultadas': cedulas_consultadas,
            'categorias': {},  # Podrías calcular categorías si quieres
            'ultimas_consultas': ultimas_consultas,
            'positivas': positivas,
            'negativas': negativas
        }

        return jsonify({
            'total_contratistas_unicos': cedulas_unicas,
            'total_contratos': total_contratos,
            'promedio_contratos': promedio,
            'chat': chat_data,
            'estados': estados_data,
            'tipos_problemas': tipos_problemas,
            'por_anio': por_anio,
            'top_problemas': top_problemas,
            'sin_movimiento': [],
            'contratistas': []
        })
    except Exception as e:
        print(f"Error en supervisor_dashboard: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


# ==================== INICIO DEL SERVIDOR ====================

if __name__ == '__main__':
    print("=" * 50)
    print("Chatbot CONTRATISTAS activo")
    print("Chat:         http://localhost:5000")
    print("Consultas:    http://localhost:5000/consultas")
    print("Buscar:       http://localhost:5000/buscar")
    print("Login:        http://localhost:5000/login")
    print("Admin:        http://localhost:5000/admin")
    print("Supervisor:   http://localhost:5000/supervisor")
    print("=" * 50)
    app.run(debug=True, port=5000)