"""
Chatbot de Contratación - API Completa
Arquitectura: Embeddings (Sentence-BERT) + IA Generativa (Llama 3.1) + Excel
Versión con mejoras de seguridad: bcrypt, cookies seguras, CORS restringido, rate limiting
"""
import os
import sys
import uuid
import hashlib
import time
import logging
import re
import jwt
from datetime import datetime, timedelta
from functools import wraps
from collections import defaultdict
from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
import pandas as pd
import bcrypt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from contratacion.lector_seguimiento import lector_seguimiento
from flask import request, jsonify
from dotenv import load_dotenv
import re
from datetime import datetime

load_dotenv()

JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'clave_por_defecto_solo_para_desarrollo')

# ==================== FUNCIÓN PARA LIMPIAR EL OBJETO DEL CONTRATO ====================
def limpiar_objeto(objeto):
    """
    Limpia el objeto del contrato:
    - Elimina saltos de línea extraños
    - Elimina espacios dobles
    - Formatea el texto legiblemente
    """
    if not objeto:
        return "Prestación de servicios profesionales como experto disciplinar."
    
    # Convertir a string
    texto = str(objeto)
    
    # Reemplazar saltos de línea por un espacio
    texto = texto.replace('\n', ' ').replace('\r', ' ')
    
    # Eliminar múltiples espacios
    texto = re.sub(r'\s+', ' ', texto)
    
    # Eliminar espacios al inicio y final
    texto = texto.strip()
    
    # Si está vacío después de limpiar, devolver texto por defecto
    if not texto:
        return "Prestación de servicios profesionales como experto disciplinar."
    
    return texto

# ==================== CARGAR .ENV ====================
try:
    from dotenv import load_dotenv
    if os.path.exists('hola.env'):
        load_dotenv('hola.env')
        print("✅ Archivo hola.env cargado correctamente (local)")
    else:
        load_dotenv()
        print("⚠️ No se encontró hola.env, intentando con .env")
except:
    print("⚠️ python-dotenv no instalado o no disponible")

# ==================== CONFIGURACIÓN SMTP ====================
SMTP_HOST = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
SMTP_USER = os.environ.get('SMTP_USER', '')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')
SMTP_FROM = os.environ.get('SMTP_FROM', SMTP_USER)

print("=" * 50)
print("🔍 CONFIGURACIÓN SMTP:")
print(f"  SMTP_HOST: {SMTP_HOST}")
print(f"  SMTP_PORT: {SMTP_PORT}")
print(f"  SMTP_USER: {SMTP_USER}")
print(f"  SMTP_FROM: {SMTP_FROM}")
print(f"  SMTP_PASSWORD: {'*' * 10 if SMTP_PASSWORD else '❌ NO CONFIGURADA'}")
print("=" * 50)

# ==================== LOGGING ====================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ==================== IMPORTS DEL PROYECTO ====================
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db import get_connection, init_db
from chatbot.orquestador import responder
from contratacion.lector import lector
from contratacion.intérprete import traducir_observacion, traducir_estado

def generar_token(usuario_id, usuario_nombre, rol):
    """
    Genera un token JWT con la información del usuario.
    """
    payload = {
        'id': usuario_id,
        'nombre': usuario_nombre,
        'rol': rol,
        'exp': datetime.utcnow() + timedelta(hours=24)  # El token expira en 24 horas
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
    return token

def verificar_token(token):
    """
    Verifica si el token es válido y devuelve el payload.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expirado
    except jwt.InvalidTokenError:
        return None  # Token inválido

def generar_token(usuario_id, usuario_nombre, rol):
    """
    Genera un token JWT con la información del usuario.
    """
    payload = {
        'id': usuario_id,
        'nombre': usuario_nombre,
        'rol': rol,
        'exp': datetime.utcnow() + timedelta(hours=24)  # El token expira en 24 horas
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
    return token

def verificar_token(token):
    """
    Verifica si el token es válido y devuelve el payload.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expirado
    except jwt.InvalidTokenError:
        return None  # Token inválido

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Buscar el token en el encabezado Authorization
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'error': 'Token no proporcionado'}), 401
        
        payload = verificar_token(token)
        if not payload:
            return jsonify({'error': 'Token inválido o expirado'}), 401
        
        # Agregar el payload a la petición para usarlo en la ruta
        request.jwt_payload = payload
        return f(*args, **kwargs)
    
    return decorated

# ==================== FUNCIÓN ENVIAR CORREO ====================
def enviar_correo(destinatario, asunto, cuerpo):
    """
    Envía un correo usando SMTP.
    Retorna (exito: bool, mensaje: str)
    """
    if not SMTP_USER or not SMTP_PASSWORD:
        print("⚠️ Credenciales SMTP no configuradas")
        return False, "Credenciales SMTP no configuradas"
    
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_FROM
        msg['To'] = destinatario
        msg['Subject'] = asunto
        msg.attach(MIMEText(cuerpo, 'html' if '<' in cuerpo else 'plain', 'utf-8'))

        print(f"📤 Conectando a {SMTP_HOST}:{SMTP_PORT}...")
        
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.connect(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Correo enviado a {destinatario}")
        return True, "Correo enviado correctamente"
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Error de autenticación: {e}")
        return False, f"Error de autenticación: Verifica usuario/contraseña (error: {str(e)})"
    except Exception as e:
        print(f"❌ Error enviando correo: {e}")
        return False, str(e)

# ==================== CONFIGURACIÓN DE FLASK ====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')
STATIC_DIR = os.path.join(FRONTEND_DIR, 'static')

app = Flask(__name__, static_folder=STATIC_DIR, static_url_path='/static')
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

# Seguridad de cookies
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
app.config['SESSION_COOKIE_DOMAIN'] = None

# CORS restringido
allowed_origins = [
    "http://localhost:5000",
    "https://chatbot-contratistas.onrender.com",
]
CORS(app, origins=allowed_origins, supports_credentials=True)

print(f"Frontend sirviendo desde: {FRONTEND_DIR}")
print(f"Estáticos sirviendo desde: {STATIC_DIR}")
print(f"CSS existe: {os.path.exists(os.path.join(STATIC_DIR, 'css', 'estilos.css'))}")

# Inicializar base de datos
init_db()

# ==================== RATE LIMITING ====================
login_attempts = defaultdict(list)

# ==================== DECORADOR ADMIN_REQUIRED ====================
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'admin_id' not in session:
            return jsonify({'error': 'No autorizado'}), 401
        return f(*args, **kwargs)
    return decorated

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

@app.route('/rut')
def validador_rut():
    return send_from_directory(FRONTEND_DIR, 'rut.html')

# ==================== PRUEBA DE CORREO ====================
@app.route('/api/admin/test-correo', methods=['POST'])
@admin_required
def test_correo():
    """Endpoint para probar el envío de correos"""
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Datos inválidos'}), 400
    
    destinatario = data.get('destinatario', '').strip()
    if not destinatario:
        return jsonify({'success': False, 'error': 'Falta destinatario'}), 400
    
    asunto = "🧪 Prueba de correo - Chatbot UNIMINUTO"
    cuerpo = f"""
    <h2>¡Correo de prueba exitoso! ✅</h2>
    <p>Este es un correo de prueba enviado desde el sistema de contratación de UNIMINUTO Virtual.</p>
    <p>Si estás viendo esto, el sistema de correos está funcionando correctamente.</p>
    <hr>
    <p style="color: #666; font-size: 0.9em;">Este es un mensaje automático, por favor no responder.</p>
    """
    
    exito, mensaje = enviar_correo(destinatario, asunto, cuerpo)
    
    if exito:
        return jsonify({
            'success': True,
            'message': f'Correo enviado a {destinatario}',
            'detalle': mensaje
        })
    else:
        return jsonify({
            'success': False,
            'error': mensaje
        }), 500

# ==================== ENVÍO DE CORREOS (COPIAR Y PEGAR - CON FILTRO) ====================
@app.route('/api/admin/enviar-correos-pegados', methods=['POST'])
@admin_required
def enviar_correos_pegados():
    """Endpoint para enviar correos con filtro (cédula + correo)"""
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Datos inválidos'}), 400
    
    asunto = data.get('asunto', '').strip()
    destinatarios = data.get('destinatarios', [])
    
    if not asunto:
        return jsonify({'success': False, 'error': 'Falta el asunto'}), 400
    
    if not destinatarios or not isinstance(destinatarios, list):
        return jsonify({'success': False, 'error': 'Lista de destinatarios vacía'}), 400
    
    if len(destinatarios) > 500:
        return jsonify({'success': False, 'error': 'Demasiados destinatarios (máximo 500)'}), 400

    PLANTILLA_CON_REGISTRO = """
    Buen día, {nombre}

    Solicitamos su colaboración con el registro en el PORTAL DE PROVEEDORES DE UNIMINUTO, a continuación, compartimos el enlace para efectuar su inscripción como proveedor de UNIMINUTO (ver video adjunto e instructivo)

    👉 Enlace portal de proveedores: https://proveedores.uniminuto.edu

    Es importante tener en cuenta lo siguiente al momento del registro:
    - Seleccionar la Sede de Operaciones: Rectoría UNIMINUTO Virtual.
    - En la opción Bien o Servicio, seleccionar Servicio y posteriormente la categoría correspondiente.
    - En el apartado 24 de su RUT se indica el tipo de contribuyente el cual debe coincidir con el registro en el portal.
    - Régimen: Persona Natural → Simplificado, Persona Jurídica → Común.
    - Tratamiento: Señor(a) → si no es colaborador; Empleado(a) → solo si es colaborador UNIMINUTO.

    Así mismo, agradecemos enviar la siguiente documentación en formato PDF y sin contraseñas para proceder con los trámites internos requeridos para el proceso de contratación por prestación de servicios solicitado por UNIMINUTO VIRTUAL:

    Documentos mínimos requeridos:
    - Cédula de ciudadanía.
    - Certificación bancaria con fecha de expedición no mayor a 30 días.
    - Cotización firmada y en formato PDF.
    - RUT actualizado con fecha de expedición no mayor a 30 días. La actividad económica registrada debe corresponder a la labor a desarrollar; en caso de no contar con una actividad específica, se sugiere utilizar el código 8560 – Actividades de apoyo a la educación.
    - Formato Excel adjunto debidamente diligenciado.
    - Certificación de afiliación a ARL activa como trabajador independiente.
    - Examen médico ocupacional (máxima vigencia de 3 años).

    ✨IMPORTANTE:
    🧮 Recuerde que el NO REGISTRO EFECTIVO en el portal de proveedores o la falta de alguno de los documentos anteriormente solicitados generará retrazos y afectaciones en el proceso de contratación el cual se notificará al supervisor del proyecto.
    🔎 Al momento de la recepción de este correo debe realizar su registro y envio de documentos de manera inmediata.

    ✨OBJETO DEL CONTRATO:
    {objeto}

    FECHA DE INICIO: {fecha_inicio}
    FECHA FIN: {fecha_fin}

    Quedo atenta a sus comentarios.

    Cordialmente,
    """

    PLANTILLA_SIN_REGISTRO = """
    Buen día, {nombre}

    Solicitamos su colaboración envio de la siguiente documentación en formato PDF y sin contraseñas para proceder con los tramites internos requeridos para el proceso de contratación por prestación de servicios solicitado por UNIMINUTO VIRTUAL:

    Documentos mínimos requeridos:
    - Cédula de ciudadanía.
    - Certificación bancaria con fecha de expedición no mayor a 30 días.
    - Cotización firmada y en formato PDF.
    - RUT actualizado con fecha de expedición no mayor a 30 días. La actividad económica registrada debe corresponder a la labor a desarrollar; en caso de no contar con una actividad específica, se sugiere utilizar el código 8560 – Actividades de apoyo a la educación.
    - Formato Excel adjunto debidamente diligenciado.
    - Certificación de afiliación a ARL activa como trabajador independiente.
    - Examen médico ocupacional (máxima vigencia de 3 años).

    ✨IMPORTANTE:
    🧮 Recuerde que la falta de alguno de los documentos anteriormente solicitados generará retrazos y afectaciones en el proceso de contratación el cual se notificará al supervisor del proyecto.

    ✨OBJETO DEL CONTRATO:
    {objeto}

    FECHA DE INICIO: {fecha_inicio}
    FECHA FIN: {fecha_fin}

    Quedo atenta a sus comentarios.

    Cordialmente,
    """

    exitosos = 0
    fallidos = 0
    errores = []
    con_registro = 0
    sin_registro = 0
    
    for item in destinatarios:
        cedula = item.get('cedula', '').strip()
        correo = item.get('correo', '').strip()
        
        if not cedula or not correo or '@' not in correo:
            fallidos += 1
            errores.append(f"Datos inválidos: {item}")
            continue
        
        # Limpiar cédula
        cedula_limpia = re.sub(r'["\'\.\s,;]', '', str(cedula))
        if re.search(r'\d{1,3}\.\d{3}\.\d{3}', cedula_limpia):
            cedula_limpia = re.sub(r'\.', '', cedula_limpia)
        if re.search(r'\d{6,12}\s+[a-zA-Z]', cedula_limpia):
            cedula_limpia = re.sub(r'\s+[a-zA-Z].*$', '', cedula_limpia)
        
        if not re.match(r'^\d{6,12}$', cedula_limpia):
            fallidos += 1
            errores.append(f"Cédula inválida: {cedula}")
            continue
        
        registros = lector.buscar_por_cedula(cedula_limpia)
        tiene_contrato = registros is not None and len(registros) > 0
        
        nombre = "Contratista"
        fecha_inicio = "01/08/2026"
        fecha_fin = "31/12/2026"
        objeto = "Prestación de servicios profesionales como experto disciplinar para la construcción de documentos de obtención de registro calificado."
        
        if tiene_contrato:
            info = lector.obtener_info_contratista(registros[0])
            nombre = info.get('nombre', nombre)
            if info.get('fecha_inicio'):
                fecha_inicio = info.get('fecha_inicio')
            if info.get('fecha_fin'):
                fecha_fin = info.get('fecha_fin')
            if info.get('objeto'):
                objeto = info.get('objeto')
        
        if tiene_contrato:
            plantilla = PLANTILLA_SIN_REGISTRO
            sin_registro += 1
        else:
            plantilla = PLANTILLA_CON_REGISTRO
            con_registro += 1
        
        cuerpo = plantilla.format(
            nombre=nombre,
            objeto=objeto,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        
        exito, mensaje = enviar_correo(correo, asunto, cuerpo)
        if exito:
            exitosos += 1
        else:
            fallidos += 1
            errores.append(f"{correo}: {mensaje}")
    
    logging.info(f"Correos enviados: {exitosos} exitosos, {fallidos} fallidos | Con registro: {con_registro}, Sin registro: {sin_registro}")
    
    return jsonify({
        'success': True,
        'exitosos': exitosos,
        'fallidos': fallidos,
        'con_registro': con_registro,
        'sin_registro': sin_registro,
        'errores': errores[:10]
    })

# ==================== ENVÍO DE CORREOS SIN FILTRO ====================
@app.route('/api/admin/enviar-correos-sin-filtro', methods=['POST'])
@admin_required
def enviar_correos_sin_filtro():
    """Endpoint para enviar correos sin filtro (solo correos)"""
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Datos inválidos'}), 400
    
    asunto = data.get('asunto', '').strip()
    destinatarios = data.get('destinatarios', [])
    plantilla = data.get('plantilla', 'con_registro')
    
    if not asunto:
        return jsonify({'success': False, 'error': 'Falta el asunto'}), 400
    
    if not destinatarios or not isinstance(destinatarios, list):
        return jsonify({'success': False, 'error': 'Lista de destinatarios vacía'}), 400
    
    if len(destinatarios) > 500:
        return jsonify({'success': False, 'error': 'Demasiados destinatarios (máximo 500)'}), 400

    PLANTILLA_CON_REGISTRO = """
    Buen día,

    Solicitamos su colaboración con el registro en el PORTAL DE PROVEEDORES DE UNIMINUTO, a continuación, compartimos el enlace para efectuar su inscripción como proveedor de UNIMINUTO (ver video adjunto e instructivo)

    👉 Enlace portal de proveedores: https://proveedores.uniminuto.edu

    Es importante tener en cuenta lo siguiente al momento del registro:
    - Seleccionar la Sede de Operaciones: Rectoría UNIMINUTO Virtual.
    - En la opción Bien o Servicio, seleccionar Servicio y posteriormente la categoría correspondiente.
    - En el apartado 24 de su RUT se indica el tipo de contribuyente el cual debe coincidir con el registro en el portal.
    - Régimen: Persona Natural → Simplificado, Persona Jurídica → Común.
    - Tratamiento: Señor(a) → si no es colaborador; Empleado(a) → solo si es colaborador UNIMINUTO.

    Así mismo, agradecemos enviar la siguiente documentación en formato PDF y sin contraseñas para proceder con los trámites internos requeridos para el proceso de contratación por prestación de servicios solicitado por UNIMINUTO VIRTUAL:

    Documentos mínimos requeridos:
    - Cédula de ciudadanía.
    - Certificación bancaria con fecha de expedición no mayor a 30 días.
    - Cotización firmada y en formato PDF.
    - RUT actualizado con fecha de expedición no mayor a 30 días. La actividad económica registrada debe corresponder a la labor a desarrollar; en caso de no contar con una actividad específica, se sugiere utilizar el código 8560 – Actividades de apoyo a la educación.
    - Formato Excel adjunto debidamente diligenciado.
    - Certificación de afiliación a ARL activa como trabajador independiente.
    - Examen médico ocupacional (máxima vigencia de 3 años).

    ✨IMPORTANTE:
    🧮 Recuerde que el NO REGISTRO EFECTIVO en el portal de proveedores o la falta de alguno de los documentos anteriormente solicitados generará retrazos y afectaciones en el proceso de contratación el cual se notificará al supervisor del proyecto.
    🔎 Al momento de la recepción de este correo debe realizar su registro y envio de documentos de manera inmediata.

    ✨OBJETO DEL CONTRATO:
    {objeto}

    FECHA DE INICIO: {fecha_inicio}
    FECHA FIN: {fecha_fin}

    Quedo atenta a sus comentarios.

    Cordialmente,
    """

    PLANTILLA_SIN_REGISTRO = """
    Buen día,

    Solicitamos su colaboración envio de la siguiente documentación en formato PDF y sin contraseñas para proceder con los tramites internos requeridos para el proceso de contratación por prestación de servicios solicitado por UNIMINUTO VIRTUAL:

    Documentos mínimos requeridos:
    - Cédula de ciudadanía.
    - Certificación bancaria con fecha de expedición no mayor a 30 días.
    - Cotización firmada y en formato PDF.
    - RUT actualizado con fecha de expedición no mayor a 30 días. La actividad económica registrada debe corresponder a la labor a desarrollar; en caso de no contar con una actividad específica, se sugiere utilizar el código 8560 – Actividades de apoyo a la educación.
    - Formato Excel adjunto debidamente diligenciado.
    - Certificación de afiliación a ARL activa como trabajador independiente.
    - Examen médico ocupacional (máxima vigencia de 3 años).

    ✨IMPORTANTE:
    🧮 Recuerde que la falta de alguno de los documentos anteriormente solicitados generará retrazos y afectaciones en el proceso de contratación el cual se notificará al supervisor del proyecto.

    ✨OBJETO DEL CONTRATO:
    {objeto}

    FECHA DE INICIO: {fecha_inicio}
    FECHA FIN: {fecha_fin}

    Quedo atenta a sus comentarios.

    Cordialmente,
    """
    
    plantilla_cuerpo = PLANTILLA_CON_REGISTRO if plantilla == 'con_registro' else PLANTILLA_SIN_REGISTRO
    
    exitosos = 0
    fallidos = 0
    errores = []
    
    for correo in destinatarios:
        if not correo or '@' not in correo:
            fallidos += 1
            errores.append(f"Correo inválido: {correo}")
            continue
        
        nombre = "Contratista"
        objeto = "Prestación de servicios profesionales como experto disciplinar para la construcción de documentos de obtención de registro calificado."
        fecha_inicio = "01/08/2026"
        fecha_fin = "31/12/2026"
        
        cuerpo = plantilla_cuerpo.format(
            nombre=nombre,
            objeto=objeto,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        
        exito, mensaje = enviar_correo(correo, asunto, cuerpo)
        if exito:
            exitosos += 1
        else:
            fallidos += 1
            errores.append(f"{correo}: {mensaje}")
    
    logging.info(f"Correos sin filtro enviados: {exitosos} exitosos, {fallidos} fallidos")
    
    return jsonify({
        'success': True,
        'exitosos': exitosos,
        'fallidos': fallidos,
        'errores': errores[:10]
    })

# ==================== API CHAT ====================
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    pregunta = data.get('mensaje', '').strip()
    usuario = data.get('usuario', f'anonimo_{uuid.uuid4().hex[:8]}')

    if not pregunta:
        return jsonify({'error': 'Mensaje vacio'}), 400

    respuesta = responder(pregunta, usuario=usuario)
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
    
    ip = request.remote_addr
    now = datetime.now()
    login_attempts[ip] = [t for t in login_attempts[ip] if now - t < timedelta(minutes=5)]
    if len(login_attempts[ip]) >= 5:
        logging.warning(f"Rate limit excedido para IP {ip}")
        return jsonify({'success': False, 'error': 'Demasiados intentos. Espera 5 minutos.'}), 429
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM administradores WHERE usuario = ?', (usuario,))
        admin = cursor.fetchone()
        conn.close()
        
        if not admin:
            login_attempts[ip].append(now)
            logging.warning(f"Login fallido: usuario '{usuario}' no existe desde {request.remote_addr}")
            return jsonify({'success': False, 'error': 'Credenciales inválidas'}), 401
        
        try:
            if bcrypt.checkpw(contrasena.encode(), admin['contrasena'].encode()):
                login_attempts[ip] = []
                
                # Generar el token JWT
                token = generar_token(
                    usuario_id=admin['id'],
                    usuario_nombre=admin['nombre'],
                    rol=admin['usuario']  # 'admin' o 'supervisor'
                )
                
                logging.info(f"Login exitoso: {usuario} desde {request.remote_addr}")
                
                return jsonify({
                    'success': True,
                    'token': token,
                    'admin': {
                        'id': admin['id'],
                        'usuario': admin['usuario'],
                        'nombre': admin['nombre'],
                        'rol': admin['usuario']
                    }
                })
        except ValueError:
            import hashlib
            contrasena_hash_sha256 = hashlib.sha256(contrasena.encode()).hexdigest()
            if admin['contrasena'] == contrasena_hash_sha256:
                nuevo_hash = bcrypt.hashpw(contrasena.encode(), bcrypt.gensalt()).decode()
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute('UPDATE administradores SET contrasena = ? WHERE id = ?', (nuevo_hash, admin['id']))
                conn.commit()
                conn.close()
                
                login_attempts[ip] = []
                
                token = generar_token(
                    usuario_id=admin['id'],
                    usuario_nombre=admin['nombre'],
                    rol=admin['usuario']
                )
                
                logging.info(f"Login exitoso (migrado a bcrypt): {usuario} desde {request.remote_addr}")
                
                return jsonify({
                    'success': True,
                    'token': token,
                    'admin': {
                        'id': admin['id'],
                        'usuario': admin['usuario'],
                        'nombre': admin['nombre'],
                        'rol': admin['usuario']
                    }
                })
        
        login_attempts[ip].append(now)
        logging.warning(f"Login fallido: contraseña incorrecta para {usuario} desde {request.remote_addr}")
        return jsonify({'success': False, 'error': 'Credenciales inválidas'}), 401
        
    except Exception as e:
        logging.error(f"Error en login: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ==================== API CONTRATISTAS ====================
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
            # ===== USAR obtener_info_contratista PARA EXTRAER EL CONTRATO =====
            info = lector.obtener_info_contratista(r)
            
            # ===== LIMPIAR EL OBJETO DEL CONTRATO =====
            objeto_limpio = limpiar_objeto(info.get('objeto', ''))
            
            contratistas.append({
                'nombre': r.get('NOMBRE DE CONTRATISTA', 'Sin nombre'),
                'cedula': r.get('CEDULA', ''),
                'estado': r.get('ESTADO', 'Sin estado'),
                'observacion': r.get('OBSERVACIÓN', 'Sin observaciones'),
                'año': str(r.get('AÑO', '')),
                'solicitud_ariba': info.get('solicitud_ariba', ''),
                'objeto': objeto_limpio,  # <--- NUEVO CAMPO
                'tipo': 'resumen'
            })
        
        return jsonify({
            'encontrado': True,
            'cantidad': len(contratistas),
            'contratistas': contratistas
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== API MI PROCESO ====================
@app.route('/api/mi-proceso', methods=['POST'])
def mi_proceso():
    data = request.get_json()
    cedula = data.get('cedula', '').strip()
    
    if not cedula:
        return jsonify({'error': 'Necesito la cédula'}), 400
    
    try:
        registros = lector.buscar_por_cedula(cedula)
        seguimiento = lector_seguimiento.buscar_por_cedula(cedula)
        contratistas = []
        
        if registros:
            for r in registros:
                # ===== OBTENER INFO COMPLETA DEL LECTOR =====
                info = lector.obtener_info_contratista(r)
                
                estado_original = r.get('ESTADO', 'Sin estado')
                estado_traducido = traducir_estado(estado_original)
                if not estado_traducido:
                    estado_traducido = f"📋 {estado_original}"
                
                obs_original = r.get('OBSERVACIÓN', '')
                obs_traducida = traducir_observacion(obs_original)
                if not obs_traducida or len(obs_traducida) < 10:
                    if obs_original and str(obs_original).lower() not in ['nan', 'none', '']:
                        obs_traducida = f"📋 {obs_original}"
                    else:
                        obs_traducida = "📋 Sin información adicional"
                
                # ===== LIMPIAR EL OBJETO DEL CONTRATO =====
                objeto_limpio = limpiar_objeto(info.get('objeto', ''))
                
                contratistas.append({
                    'nombre': info.get('nombre', 'Sin nombre'),
                    'cedula': info.get('cedula', cedula),
                    'estado': estado_traducido,
                    'observacion': obs_traducida,
                    'año': info.get('año', ''),
                    'solicitud_ariba': info.get('solicitud_ariba', '-'),
                    'objeto': objeto_limpio,  # <--- NUEVO CAMPO
                    'tipo': 'resumen'
                })
        
        if seguimiento:
            solpedidos = {}
            for s in seguimiento:
                solpedido = str(s.get('SOLPEDIDO', 'Desconocido'))
                if solpedido not in solpedidos:
                    solpedidos[solpedido] = {
                        'solpedido': solpedido,
                        'nombre': s.get('NOMBRE DEL PROVEEDOR', 'Sin nombre'),
                        'cedula': s.get('CEDULA', cedula),
                        'pagos': []
                    }
                
                info_pos = lector_seguimiento.extraer_info_pos(s.get('TEXTO DE POS', ''))
                estado = s.get('ESTADO SOLPEDIDO', 'Sin estado')
                
                solpedidos[solpedido]['pagos'].append({
                    'pos': str(s.get('POS', '')),
                    'estado': estado,
                    'observacion': s.get('OBSERVACIÓN SOLPEDIDO', 'Sin observaciones'),
                    'tipo_pago': info_pos.get('tipo_pago', 'Pago'),
                    'mes': info_pos.get('mes', ''),
                    'objeto': info_pos.get('objeto', ''),
                    'valor': s.get('VALOR TOTAL', 0),
                    'es_eliminado': 'Eliminado' in str(estado) or 'ELIMINADO' in str(estado).upper()
                })
            
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

# ==================== VALIDAR RUT ====================
@app.route('/api/validar-rut', methods=['POST'])
def validar_rut():
    from werkzeug.utils import secure_filename
    from contratacion.validador_rut import validar_rut_archivo    
    
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
    
    contratista_info = None
    if cedula:
        try:
            registros = lector.buscar_por_cedula(cedula)
            if registros:
                contratista_info = lector.obtener_info_contratista(registros[0])
        except:
            pass
    
    UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    nombre_seguro = secure_filename(archivo.filename)
    ruta_archivo = os.path.join(UPLOAD_DIR, nombre_seguro)
    archivo.save(ruta_archivo)
    
    try:
        respuesta, resultado = validar_rut_archivo(ruta_archivo, cedula)
        
        if contratista_info:
            resultado['datos_extraidos']['nombre_contratista'] = contratista_info.get('nombre')
            resultado['datos_extraidos']['cedula_contratista'] = contratista_info.get('cedula')
        
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

# ==================== LOGIN CON BCRYPT Y RATE LIMITING ====================
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

# ==================== SUPERVISOR DASHBOARD ====================
@app.route('/api/supervisor/dashboard', methods=['GET'])
@admin_required
def supervisor_dashboard():
    import traceback
    try:
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
                'contratistas': [],
                'seguimiento': {'total_solpedidos': 0, 'total_posiciones': 0, 'estados': {}, 'eliminados': 0, 'activos': 0}
            })

        total_contratos = len(df)
        cedulas_unicas = df['CEDULA'].nunique() if 'CEDULA' in df.columns else 0
        promedio = round(total_contratos / cedulas_unicas, 2) if cedulas_unicas > 0 else 0

        if 'ESTADO' in df.columns:
            estados_counts = df['ESTADO'].value_counts().head(10)
            estados_data = {
                'labels': estados_counts.index.tolist(),
                'values': estados_counts.values.tolist()
            }
        else:
            estados_data = {'labels': [], 'values': []}

        if 'AÑO' in df.columns:
            anios_counts = df['AÑO'].value_counts()
            por_anio = {str(k): v for k, v in anios_counts.items() if pd.notna(k)}
        else:
            por_anio = {}

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

        seguimiento_df = lector_seguimiento.df
        seguimiento_stats = {}
        if seguimiento_df is not None and not seguimiento_df.empty:
            total_solpedidos = seguimiento_df['SOLPEDIDO'].nunique()
            total_posiciones = len(seguimiento_df)
            estados_solpedido = seguimiento_df['ESTADO SOLPEDIDO'].value_counts().to_dict()
            eliminados = seguimiento_df[seguimiento_df['ESTADO SOLPEDIDO'].str.upper().str.contains('ELIMINADO', na=False)].shape[0]
            seguimiento_stats = {
                'total_solpedidos': total_solpedidos,
                'total_posiciones': total_posiciones,
                'estados': estados_solpedido,
                'eliminados': eliminados,
                'activos': total_solpedidos - eliminados
            }
        else:
            seguimiento_stats = {
                'total_solpedidos': 0,
                'total_posiciones': 0,
                'estados': {},
                'eliminados': 0,
                'activos': 0
            }

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
            'categorias': {},
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
            'contratistas': [],
            'seguimiento': seguimiento_stats
        })
    except Exception as e:
        print(f"Error en supervisor_dashboard: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# ==================== SUBIR EXCEL SIN REDEPLOY ====================
@app.route('/api/admin/upload-excel', methods=['POST'])
@admin_required
def upload_excel():
    from werkzeug.utils import secure_filename
    
    if 'archivo' not in request.files:
        return jsonify({'success': False, 'error': 'No se envió ningún archivo'}), 400
    
    archivo = request.files['archivo']
    if archivo.filename == '':
        return jsonify({'success': False, 'error': 'El archivo está vacío'}), 400
    
    if not archivo.filename.lower().endswith(('.xlsx', '.xls')):
        return jsonify({'success': False, 'error': 'Solo se permiten archivos Excel (.xlsx o .xls)'}), 400
    
    nombre = archivo.filename.lower()
    if 'contratacion' in nombre or 'contratista' in nombre:
        destino = os.path.join(BASE_DIR, 'database', 'contratacion.xlsx')
        tipo = 'contratistas'
    elif 'seguimiento' in nombre:
        destino = os.path.join(BASE_DIR, 'database', 'seguimiento.xlsx')
        tipo = 'seguimiento'
    else:
        return jsonify({
            'success': False, 
            'error': 'El nombre del archivo debe contener "contratacion" o "seguimiento" para identificar su tipo.'
        }), 400
    
    try:
        archivo.save(destino)
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error al guardar el archivo: {str(e)}'}), 500
    
    try:
        if tipo == 'contratistas':
            lector.cargar_datos()
            mensaje = 'Archivo de contratistas actualizado correctamente'
        else:
            lector_seguimiento.cargar_datos()
            mensaje = 'Archivo de seguimiento actualizado correctamente'
        
        logging.info(f"Excel actualizado: {tipo} por admin desde {request.remote_addr}")
        return jsonify({
            'success': True,
            'message': mensaje,
            'tipo': tipo
        })
    except Exception as e:
        return jsonify({
            'success': False, 
            'error': f'Error al recargar los datos: {str(e)}'
        }), 500

@app.route('/api/admin/test-env', methods=['GET'])
@admin_required
def test_env():
    return jsonify({
        'SMTP_USER': os.environ.get('SMTP_USER', 'NO_CONFIGURADO'),
        'SMTP_HOST': os.environ.get('SMTP_HOST', 'NO_CONFIGURADO'),
        'SMTP_PORT': os.environ.get('SMTP_PORT', 'NO_CONFIGURADO'),
        'SMTP_FROM': os.environ.get('SMTP_FROM', 'NO_CONFIGURADO'),
        'SECRET_KEY': os.environ.get('SECRET_KEY', 'NO_CONFIGURADO')[:10] + '...' if os.environ.get('SECRET_KEY') else 'NO_CONFIGURADO'
    })

# ==================== CABECERAS DE SEGURIDAD ====================
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    return response

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
    print("RUT:          http://localhost:5000/rut")
    print("=" * 50)
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, port=5000)