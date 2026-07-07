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
    """Devuelve el estado del contratista con observaciones"""
    data = request.get_json()
    cedula = data.get('cedula', '').strip()
    
    if not cedula:
        return jsonify({'error': 'Necesito la cédula'}), 400
    
    try:
        registros = lector.buscar_por_cedula(cedula)
        
        if not registros:
            return jsonify({
                'encontrado': False,
                'mensaje': f'No encontré información con la cédula {cedula}. Verifica que esté bien escrita.'
            })
        
        contratistas = []
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
                'año': str(r.get('AÑO', ''))
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
    from contratacion.validador_rut import analizar_rut
    import os
    
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
        # Analizar RUT
        resultado = analizar_rut(ruta_archivo, cedula)
        
        # Agregar info del contratista
        if contratista_info:
            resultado['datos']['nombre_contratista'] = contratista_info.get('nombre')
            resultado['datos']['cedula_contratista'] = contratista_info.get('cedula')
        
        # Generar texto legible
        texto = generar_texto_rut(resultado, contratista_info)
        
        # Limpiar
        try:
            os.remove(ruta_archivo)
        except:
            pass
        
        return jsonify({
            'success': True,
            'valido': resultado['valido'],
            'datos': resultado['datos'],
            'errores': resultado['errores'],
            'advertencias': resultado['advertencias'],
            'exitos': resultado['exitos'],
            'respuesta_legible': texto,
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


def generar_texto_rut(resultado, contratista_info=None):
    """Convierte el resultado a texto legible"""
    lineas = []
    
    if contratista_info and contratista_info.get('nombre'):
        lineas.append(f"👤 **Contratista:** {contratista_info['nombre']}")
    if contratista_info and contratista_info.get('cedula'):
        lineas.append(f"🆔 **Cédula:** {contratista_info['cedula']}")
    lineas.append("")
    
    lineas.append("📄 **Resultado del análisis de tu RUT**")
    lineas.append("─" * 30)
    lineas.append("")
    
    datos = resultado.get('datos', {})
    if datos:
        lineas.append("📋 **Datos extraídos del RUT:**")
        if datos.get('nombre'):
            lineas.append(f"  • Nombre: {datos['nombre']}")
        if datos.get('cedula'):
            lineas.append(f"  • Cédula: {datos['cedula']}")
        if datos.get('correo'):
            lineas.append(f"  • Correo: {datos['correo']}")
        if datos.get('actividad'):
            act_nom = datos.get('actividad_nombre', '')
            lineas.append(f"  • Actividad: {datos['actividad']} ({act_nom})")
        if datos.get('fecha'):
            lineas.append(f"  • Fecha: {datos['fecha']}")
        lineas.append("")
    
    if resultado['valido']:
        lineas.append("✅ **¡Tu RUT está listo para subir a la plataforma!**")
        lineas.append("")
        for e in resultado['exitos']:
            lineas.append(f"  {e}")
    else:
        lineas.append("⚠️ **Tu RUT tiene problemas que debes corregir:**")
        lineas.append("")
        for e in resultado['errores']:
            lineas.append(f"  {e}")
        
        if resultado['advertencias']:
            lineas.append("")
            lineas.append("⚠️ **Advertencias:**")
            for a in resultado['advertencias']:
                lineas.append(f"  {a}")
        
        lineas.append("")
        lineas.append("📌 **¿Qué hacer?**")
        if any('trámite' in e.lower() or 'tramite' in e.lower() for e in resultado['errores']):
            lineas.append("  • Espera a tener 'Actualización', no 'en trámite'")
        if any('actividad' in e.lower() for e in resultado['errores']):
            lineas.append("  • Agrega actividad económica 8560 en la DIAN")
        if any('año' in e.lower() or 'antiguo' in e.lower() or 'reciente' in e.lower() for e in resultado['errores']):
            lineas.append("  • Saca un RUT actualizado (de este año o el pasado)")
        if any('cédula' in e.lower() or 'cedula' in e.lower() for e in resultado['errores']):
            lineas.append("  • Verifica que el RUT sea tuyo")
    
    return "\n".join(lineas)


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


# ==================== ENDPOINT DEL SUPERVISOR ====================

@app.route('/api/supervisor/dashboard', methods=['GET'])
@admin_required
def supervisor_dashboard():
    import traceback
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(DISTINCT CEDULA) as total FROM contratacion')
        total_contratistas_unicos = cursor.fetchone()['total']
        cursor.execute('SELECT COUNT(*) as total FROM contratacion')
        total_contratos = cursor.fetchone()['total']
        promedio = round(total_contratos / total_contratistas_unicos, 2) if total_contratistas_unicos > 0 else 0
        
        cursor.execute('SELECT COUNT(*) as total FROM consultas')
        total_chat_consultas = cursor.fetchone()['total']
        cursor.execute('SELECT COUNT(DISTINCT usuario) as unicos FROM consultas')
        usuarios_unicos = cursor.fetchone()['unicos']
        cursor.execute("SELECT COUNT(*) as total FROM consultas WHERE pregunta GLOB '[0-9][0-9][0-9][0-9][0-9][0-9]*'")
        cedulas_consultadas = cursor.fetchone()['total']
        
        cursor.execute('SELECT pregunta FROM consultas')
        todas_preguntas = cursor.fetchall()
        categorias = {'documentos': 0, 'portal': 0, 'rut': 0, 'pagos': 0, 'problemas': 0, 'llenar': 0}
        for row in todas_preguntas:
            pregunta = (row['pregunta'] or '').lower()
            if any(p in pregunta for p in ['documento', 'papel', 'que necesito']):
                categorias['documentos'] += 1
            if any(p in pregunta for p in ['portal', 'plataforma', 'registro']):
                categorias['portal'] += 1
            if 'rut' in pregunta:
                categorias['rut'] += 1
            if any(p in pregunta for p in ['pago', 'factura']):
                categorias['pagos'] += 1
            if any(p in pregunta for p in ['problema', 'error', 'no puedo']):
                categorias['problemas'] += 1
            if any(p in pregunta for p in ['llenar', 'campo']):
                categorias['llenar'] += 1
        
        # Últimas consultas del chatbot
        cursor.execute('SELECT * FROM consultas ORDER BY fecha DESC LIMIT 50')
        ultimas_consultas = [dict(row) for row in cursor.fetchall()]
        
        cursor.execute("SELECT COUNT(*) FROM consultas WHERE calificacion >= 4")
        positivas = cursor.fetchone()[0] or 0
        cursor.execute("SELECT COUNT(*) FROM consultas WHERE calificacion <= 2")
        negativas = cursor.fetchone()[0] or 0
        
        chat_data = {
            'total_consultas': total_chat_consultas,
            'usuarios_unicos': usuarios_unicos,
            'cedulas_consultadas': cedulas_consultadas,
            'categorias': categorias,
            'ultimas_consultas': ultimas_consultas,
            'positivas': positivas,
            'negativas': negativas
        }
        
        cursor.execute('''SELECT ESTADO, COUNT(*) as cantidad FROM contratacion WHERE ESTADO IS NOT NULL AND ESTADO != '' GROUP BY ESTADO ORDER BY cantidad DESC LIMIT 10''')
        estados_rows = cursor.fetchall()
        estados_data = {
            'labels': [r['ESTADO'] for r in estados_rows if r['ESTADO']],
            'values': [r['cantidad'] for r in estados_rows if r['ESTADO']]
        }
        
        cursor.execute('SELECT OBSERVACION FROM contratacion WHERE OBSERVACION IS NOT NULL')
        observaciones = cursor.fetchall()
        tipos_problemas = {
            'Rechazo en portal': 0, 'No contesta': 0, 'RUT mal/trámite': 0,
            'Régimen incorrecto': 0, 'Sede incorrecta': 0, 'Documentos pendientes': 0,
            'Documentos con clave': 0, 'Examen médico pendiente': 0,
            'Cotización pendiente': 0, 'Acta pendiente': 0, ' Otros': 0
        }
        for row in observaciones:
            obs = (row['OBSERVACION'] or '').upper()
            if not obs:
                continue
            encontrado = False
            if 'RECHAZ' in obs:
                tipos_problemas['Rechazo en portal'] += 1
                encontrado = True
            if 'NO CONTESTA' in obs:
                tipos_problemas['No contesta'] += 1
                encontrado = True
            if 'RUT' in obs and ('MAL' in obs or 'TRAMITE' in obs or 'CORRECCION' in obs):
                tipos_problemas['RUT mal/trámite'] += 1
                encontrado = True
            if 'REGIMEN' in obs:
                tipos_problemas['Régimen incorrecto'] += 1
                encontrado = True
            if 'SEDE' in obs and ('INCORRECT' in obs or 'PRINCIPAL' in obs):
                tipos_problemas['Sede incorrecta'] += 1
                encontrado = True
            if 'PTE DOCUMENTOS' in obs or 'SIN DOCUMENTOS' in obs:
                tipos_problemas['Documentos pendientes'] += 1
                encontrado = True
            if 'CONTRASEÑA' in obs or 'CON CLAVE' in obs:
                tipos_problemas['Documentos con clave'] += 1
                encontrado = True
            if 'PTE EXAMEN' in obs:
                tipos_problemas['Examen médico pendiente'] += 1
                encontrado = True
            if 'PTE COTIZACION' in obs:
                tipos_problemas['Cotización pendiente'] += 1
                encontrado = True
            if 'PTE ACTA' in obs:
                tipos_problemas['Acta pendiente'] += 1
                encontrado = True
            if not encontrado:
                tipos_problemas[' Otros'] += 1
        tipos_problemas = {k: v for k, v in tipos_problemas.items() if v > 0}
        
        cursor.execute('SELECT AÑO, COUNT(*) as cantidad FROM contratacion WHERE AÑO IS NOT NULL GROUP BY AÑO ORDER BY AÑO')
        por_anio_rows = cursor.fetchall()
        por_anio = {str(int(r['AÑO'])): r['cantidad'] for r in por_anio_rows if r['AÑO'] is not None}
        
        cursor.execute('SELECT CEDULA, NOMBRE_DE_CONTRATISTA, OBSERVACION, ESTADO FROM contratacion WHERE CEDULA IS NOT NULL AND CEDULA != \'\' LIMIT 200')
        contratistas_raw = cursor.fetchall()
        contratistas_agrupados = {}
        for row in contratistas_raw:
            cedula = row['CEDULA']
            if cedula not in contratistas_agrupados:
                contratistas_agrupados[cedula] = {
                    'cedula': cedula, 'nombre': row['NOMBRE_DE_CONTRATISTA'] or 'Sin nombre',
                    'contratos': [], 'observaciones': [], 'total_problemas': 0,
                    'tipos_problemas': Counter()
                }
            contratistas_agrupados[cedula]['contratos'].append({'estado': row['ESTADO'] or 'Sin estado'})
            obs = row['OBSERVACION'] or ''
            if obs:
                contratistas_agrupados[cedula]['observaciones'].append(obs)
                obs_upper = obs.upper()
                if 'RECHAZ' in obs_upper:
                    contratistas_agrupados[cedula]['total_problemas'] += 1
                    contratistas_agrupados[cedula]['tipos_problemas']['Rechazo'] += 1
                if 'NO CONTESTA' in obs_upper:
                    contratistas_agrupados[cedula]['total_problemas'] += 1
                    contratistas_agrupados[cedula]['tipos_problemas']['No contesta'] += 1
                if 'RUT' in obs_upper and ('MAL' in obs_upper or 'CORRECCION' in obs_upper):
                    contratistas_agrupados[cedula]['total_problemas'] += 1
                    contratistas_agrupados[cedula]['tipos_problemas']['RUT'] += 1
                if 'REGIMEN' in obs_upper:
                    contratistas_agrupados[cedula]['total_problemas'] += 1
                    contratistas_agrupados[cedula]['tipos_problemas']['Régimen'] += 1
                if 'SEDE' in obs_upper and ('INCORRECT' in obs_upper or 'PRINCIPAL' in obs_upper):
                    contratistas_agrupados[cedula]['total_problemas'] += 1
                    contratistas_agrupados[cedula]['tipos_problemas']['Sede'] += 1
                if 'PTE DOCUMENTOS' in obs_upper or 'SIN DOCUMENTOS' in obs_upper:
                    contratistas_agrupados[cedula]['total_problemas'] += 1
                    contratistas_agrupados[cedula]['tipos_problemas']['Falta docs'] += 1
                if 'CONTRASEÑA' in obs_upper or 'CON CLAVE' in obs_upper:
                    contratistas_agrupados[cedula]['total_problemas'] += 1
                    contratistas_agrupados[cedula]['tipos_problemas']['Con clave'] += 1
        
        for cedula, data_c in contratistas_agrupados.items():
            data_c['total_contratos'] = len(data_c['contratos'])
            if data_c['tipos_problemas']:
                data_c['tipo_principal'] = data_c['tipos_problemas'].most_common(1)[0][0]
            else:
                data_c['tipo_principal'] = None
        
        top_problemas = sorted(contratistas_agrupados.values(), key=lambda x: x['total_problemas'], reverse=True)[:15]
        
        cursor.execute('SELECT CEDULA, NOMBRE_DE_CONTRATISTA, ESTADO FROM contratacion WHERE CEDULA IS NOT NULL AND CEDULA != \'\' GROUP BY CEDULA, NOMBRE_DE_CONTRATISTA, ESTADO LIMIT 100')
        sin_mov_rows = cursor.fetchall()
        sin_movimiento = []
        conn.close()
        
        return jsonify({
            'total_contratistas_unicos': total_contratistas_unicos,
            'total_contratos': total_contratos, 'promedio_contratos': promedio,
            'chat': chat_data, 'estados': estados_data,
            'tipos_problemas': tipos_problemas, 'por_anio': por_anio,
            'top_problemas': top_problemas, 'sin_movimiento': sin_movimiento,
            'contratistas': list(contratistas_agrupados.values())[:500]
        })
    except Exception as e:
        print(f"Error: {e}")
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
