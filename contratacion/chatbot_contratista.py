"""
Chatbot para contratistas - Versión Final
Lenguaje claro y sencillo para todo tipo de personas
Con intérprete de observaciones y soporte para múltiples contratos
"""
import re
from .lector import lector
from .interprete import traducir_observacion, traducir_estado

# Clasificador semántico (embeddings) - se usa como RESPALDO cuando las
# reglas de palabras clave de abajo no reconocen la frase del usuario.
# Se carga perezosamente (solo la primera vez que se necesita) para no
# retrasar el arranque del servidor si nunca se llega a usar.
_clasificador_semantico = None


def _obtener_clasificador():
    global _clasificador_semantico
    if _clasificador_semantico is None:
        from nlp.embedding_classifier import EmbeddingClassifier
        _clasificador_semantico = EmbeddingClassifier()
        _clasificador_semantico.cargar_modelo()
    return _clasificador_semantico

# Links importantes
URL_PORTAL = "https://proveedores.uniminuto.edu"
URL_INSTRUCTIVO = "https://uniminuto.edu/instructivo-proveedores"
URL_FORMATO = "https://uniminuto.edu/formato-ingreso-independientes"

# Contactos
TEL_BOGOTA = "(601) 593 3004"
TEL_NACIONAL = "01 8000 11 93 90"


RESPUESTAS = {

    "saludo": """¡Hola! 👋 Soy el Asistente de Contratación de UNIMINUTO Virtual.

Para ver cómo va tu proceso, escribe tu número de cédula.

También te puedo ayudar con:
📋 Qué documentos enviar
🌐 Cómo registrarte en la plataforma
⚠️ Problemas con el registro
💰 Estado de tus pagos
📝 Problemas con el RUT

Escribe tu cédula o tu pregunta para empezar.""",

    "portal_proveedores": f"""🌐 REGISTRARTE EN LA PLATAFORMA DE PROVEEDORES

Solo tienes que entrar a este link:
👉 {URL_PORTAL}

Después llena los datos que te pide el formulario.

⚠️ Cosas importantes:
- Sede: selecciona Rectoría UNIMINUTO Virtual
- Donde dice "Bien o Servicio": elige Servicio y la categoría correspondiente
- El correo que pongas debe ser el mismo que aparece en tu RUT (ahí te vamos a mandar todo)
- Código postal: el de tu dirección de residencia

¿Tienes alguna duda con algún campo del formulario?""",

    "documentos_natural": """📋 DOCUMENTOS QUE DEBES ENVIAR (Persona Natural)

Todos los documentos deben ir en PDF y SIN CONTRASEÑA:

1. 📄 Tu cédula de ciudadanía (ambas caras)
2. 🏦 Certificación bancaria (el papel que te da el banco, no mayor a 30 días)
3. 📋 Tu RUT actualizado (no mayor a 30 días)
   - Debe decir "copia" o "certificado" como marca de agua
   - NO debe decir "en trámite"
4. 📊 El formato Excel "Ingreso Independientes" (te lo enviamos adjunto)
5. 🏥 Certificación de la ARL (donde dice que estás afiliado como independiente)
6. 🏥 Examen médico ocupacional (no mayor a 3 años de vigencia)

⚠️ Importante:
- El correo que registres en la plataforma es donde te vamos a enviar todo (desde la solicitud inicial hasta el contrato para firmar)
- Si falta algún documento o no te registras en la plataforma, tu proceso se retrasa y se le notifica a tu supervisor""",

    "documentos_juridica": """📋 DOCUMENTOS QUE DEBES ENVIAR (Empresa / Persona Jurídica)

Todos los documentos deben ir en PDF y SIN CONTRASEÑA:

1. 📄 Cédula de ciudadanía del REPRESENTANTE LEGAL
2. 🏦 Certificación bancaria de la empresa (no mayor a 30 días)
3. 📋 RUT de la empresa actualizado (no mayor a 30 días)
   - Debe decir "copia" o "certificado" como marca de agua
   - NO debe decir "en trámite"
4. 📑 Cámara de Comercio de la empresa (expedición no mayor a 30 días)
5. 📄 Cédula del representante legal en la plataforma
6. 🏥 Certificación de la ARL de la empresa
7. 🏥 Examen médico del representante legal

⚠️ Importante:
- El correo que registren en la plataforma es donde les vamos a enviar todo
- Si falta algún documento o no se registran en la plataforma, el proceso se retrasa""",

    "documentos_requeridos": """📋 DOCUMENTOS REQUERIDOS

¿Eres persona natural o empresa?

🔹 Si eres PERSONA NATURAL:
• Cédula de ciudadanía
• Certificación bancaria (menos de 30 días)
• RUT actualizado (menos de 30 días, marca de agua "copia" o "certificado")
• Formato Excel "Ingreso Independientes"
• Certificación de ARL
• Examen médico (menos de 3 años)

🔹 Si eres EMPRESA / PERSONA JURÍDICA:
• Cédula del representante legal
• Certificación bancaria de la empresa
• RUT de la empresa actualizado
• Cámara de Comercio
• Certificación de ARL de la empresa
• Examen médico del representante legal

Todos en PDF y sin contraseña.

💡 ¿Cuál es tu caso: persona natural o empresa?""",

    "actualizar_rut": """📝 CÓMO ACTUALIZAR TU RUT

Tu RUT debe estar actualizado (menos de 30 días) y debe decir "copia" o "certificado" como marca de agua. NO debe decir "en trámite".

Para actualizarlo:

1. Entra a la página de la DIAN (www.dian.gov.co)
2. Inicia sesión con tu usuario
3. Busca la opción "Actualización RUT"
4. Revisa que tus datos estén al día
5. Descarga el RUT actualizado en PDF

💡 Tip: Si vas a trabajar en educación, te recomendamos tener una actividad económica relacionada con educación, aunque la actividad específica depende de lo que vayas a hacer para UNIMINUTO.

""",

    "problemas_registro": """⚠️ ¿PROBLEMAS CON EL REGISTRO?

PROBLEMAS MÁS COMUNES:

❌ "Se rechazó mi registro"
• Probablemente elegiste mal la sede → debe ser "Rectoría UNIMINUTO Virtual"
• O el régimen está mal → debe ser "Simplificado" (persona natural) o "Común" (jurídica)
• O el tratamiento → debe ser "Señor(a)"

❌ "No me deja subir documentos"
• Verifica que los PDF NO tengan contraseña
• Prueba con Chrome o Firefox actualizados

❌ "No sé qué poner en algún campo"
• Te recomiendo descargar el instructivo y seguirlo paso a paso
• O pregúntame el campo específico que te confunde

❌ "Me equivoqué de sede"
• Solicita el rechazo al área de Servicios Integrados
• Vuelve a registrarte en la sede correcta

Si nada funciona, llama a:
📞 Bogotá: {TEL_BOGOTA}
📞 Nacional: {TEL_NACIONAL}""",

    "estado_pago": """💰 ¿CÓMO SABER SI YA TE PAGARON?

1. Revisa en la plataforma de proveedores el estado de tu factura
2. Los pagos se hacen según lo pactado en tu contrato:
   - Si es pago único: te pagan cuando termines y entregues todo bien
   - Si es pago mensual: te pagan cada mes según vayas avanzando

Estados que puedes ver:
- PTE = Pendiente (aún no se procesa)
- LIBERADO = Listo para pago
- PAGADO = Ya te transfirieron

Si tienes dudas con tu pago específico, habla con tu supervisor o con el área financiera.""",

    "llenar_plataforma": """🔧 CÓMO LLENAR BIEN LA PLATAFORMA

Cuando estés registrando, ten en cuenta estos puntos importantes:

📍 SEDE: Rectoría UNIMINUTO Virtual (es la primera parte, importante que sea esta)

🪪 TRATAMIENTO: selecciona "Señor(a)"
(Solo si eres empleado de UNIMINUTO sería "Empleado(a)")

📋 RÉGIMEN:
- Si eres persona natural → Simplificado
- Si eres empresa → Común

👤 PERSONA DE CONTACTO: pones tus propios datos (el mismo que se está inscribiendo, no otra persona)

📮 CÓDIGO POSTAL: el código postal de tu dirección de casa (búscalo en Google "código postal [tu ciudad]")

📧 CORREO: pon el mismo correo que está en tu RUT (ahí te mandaremos todo: la solicitud inicial, el contrato para firmar, etc.)

¿Dudas con algún otro campo?""",

    "fuera_de_alcance": """Disculpa, no entendí bien tu pregunta.

Puedo ayudarte con:
📋 Documentos que debes enviar
🌐 Cómo registrarte en la plataforma
🔧 Cómo llenar bien el formulario
⚠️ Problemas con el registro
📝 Actualizar el RUT
💰 Estado de tus pagos

Escribe tu cédula para ver el estado de tu proceso, o cuéntame en qué te ayudo.""",
}


def extraer_cedula(texto):
    """Saca la cédula del texto"""
    matches = re.findall(r'\b\d{6,12}\b', texto)
    for m in matches:
        if len(m) >= 7:
            return m
        if len(m) >= 6 and not m.startswith('20'):
            return m
    return None


def detectar_intencion(texto):
    """Detecta qué necesita el usuario"""
    t = texto.lower()
    cedula = extraer_cedula(texto)
    
    # Detectar intención de subir/revisar el RUT.
    # OJO: antes solo se buscaban frases EXACTAS como "subir rut", así que
    # "quiero subir MI rut" (con una palabra en el medio) no se reconocía.
    # Ahora basta con que aparezca 'rut' junto a un verbo de acción.
    _verbos_accion_rut = ['subir', 'revisar', 'validar', 'verificar', 'analizar', 'cargar', 'adjuntar', 'enviar', 'mandar']
    if 'rut' in t and any(v in t for v in _verbos_accion_rut):
        return 'subir_rut', cedula

    # Cédula tiene prioridad
    if cedula:
        return 'consulta_estado', cedula
    
    # Saludos
    if any(p in t for p in ['hola', 'buenos', 'buenas', 'hi', 'hello']):
        return 'saludo', cedula
    
    # Llenar plataforma (campos específicos)
    if any(p in t for p in ['llenar', 'como lleno', 'campos', 'persona de contacto', 'codigo ciiu', 'objeto social', 'codigo postal', 'regimen', 'tratamiento']):
        return 'llenar_plataforma', cedula
    
    # Documentos (contexto jurídico vs natural)
    if 'juridica' in t or 'empresa' in t or 'jurídica' in t or 'camara de comercio' in t or 'cámara de comercio' in t:
        return 'documentos_juridica', cedula
    
    if 'natural' in t or 'cedula' in t or 'cédula' in t or 'soy persona' in t:
        return 'documentos_natural', cedula
    
    # Documentos en general
    if any(p in t for p in ['documentos', 'que necesito', 'que papeles', 'que documentos', 'que me piden']):
        return 'documentos_requeridos', cedula
    
    # Problemas
    if any(p in t for p in ['problema', 'no puedo', 'error', 'no me deja', 'rechazo', 'rechazado', 'no funciona']):
        return 'problemas_registro', cedula
    
    # Portal
    if any(p in t for p in ['portal', 'plataforma', 'registrarme', 'registro', 'inscribirme']):
        return 'portal_proveedores', cedula
    
    # Pagos
    if any(p in t for p in ['pago', 'cobro', 'factura', 'dinero', 'me pagan', 'plata']):
        return 'estado_pago', cedula
    
    # RUT (genérico)
    if 'rut' in t:
        return 'actualizar_rut', cedula

    # Ninguna regla de palabras clave reconoció la frase: se lo preguntamos
    # al clasificador semántico antes de darnos por vencidos. Esto cubre
    # frases con otras palabras que significan lo mismo (ej. "no me deja
    # terminar la inscripción" en vez de "no puedo registrarme").
    try:
        clasificador = _obtener_clasificador()
        intencion_semantica, similitud = clasificador.predecir(texto)
        if intencion_semantica != 'fuera_de_alcance' and (intencion_semantica in RESPUESTAS or intencion_semantica == 'subir_rut'):
            return intencion_semantica, cedula
    except Exception as e:
        print(f"⚠️ Clasificador semántico no disponible: {e}")

    return 'fuera_de_alcance', cedula


def formatear_contrato(info_contrato, numero_contrato=None):
    """Formatea la info de un contrato"""
    estado_traducido = traducir_estado(info_contrato['estado'])
    
    if not estado_traducido:
        if info_contrato['estado'] and str(info_contrato['estado']).lower() not in ['nan', 'none', '']:
            estado_traducido = f"📋 {info_contrato['estado']}"
        else:
            estado_traducido = "📋 Sin estado registrado"
    
    observacion_traducida = traducir_observacion(info_contrato['observacion'])
    
    if not observacion_traducida:
        texto = info_contrato['observacion']
        if texto and str(texto).lower() not in ['nan', 'none', '']:
            observacion_traducida = f"📝 {str(texto)[:300]}"
        else:
            observacion_traducida = "📝 Sin información adicional"
    
    encabezado = ""
    if numero_contrato:
        encabezado = f"\n--- **CONTRATO #{numero_contrato}** ---\n"
    
    return f"""{encabezado}
📊 **Estado:** {estado_traducido}

{observacion_traducida}
"""


def responder_contratista(mensaje):
    """Responde al contratista"""
    intencion, cedula = detectar_intencion(mensaje)
    
    # ===== NUEVO: SUBIR RUT =====
    if intencion == 'subir_rut':
        return """📄 **Para validar tu RUT, sigue estos pasos:**

1. **Ten listo tu RUT en PDF** (que diga "copia" o "certificado", no "en trámite")
2. **Sube el archivo** usando el botón de abajo
3. **Espera el análisis** - te diré qué está bien y qué falta

📋 **Lo que voy a verificar:**
- ✅ Que diga "copia" o "certificado" (no "en trámite")
- ✅ Que tenga la actividad 8560
- ✅ Que tenga menos de 30 días de expedición
- ✅ Que la cédula coincida con la tuya

⚠️ **Importante:** Por ahora solo funciona con PDFs digitales (no escaneados como imagen).

📎 [Selecciona tu RUT en PDF para subirlo]"""
    
    # Si tiene cédula, buscar al contratista
    if cedula:
        registros = lector.buscar_por_cedula(cedula)
        
        if registros:
            info_principal = lector.obtener_info_contratista(registros[0])
            
            # Construir respuesta base
            respuesta = f"""📋 **ESTADO DE TU PROCESO**

👤 **Nombre:** {info_principal['nombre']}
🆔 **Cédula:** {info_principal['cedula']}
📅 **Año:** {info_principal['año']}

═══════════════════════════════════════
"""
            
            # Agregar info del contrato principal
            respuesta += formatear_contrato(info_principal)
            
            # Si tiene múltiples contratos
            if len(registros) > 1:
                respuesta += f"\n═══════════════════════════════════════\n"
                respuesta += f"📋 **TIENES {len(registros)} CONTRATOS REGISTRADOS**\n"
                respuesta += "═══════════════════════════════════════\n"
                
                for i, otro in enumerate(registros[1:], 2):
                    info_otro = lector.obtener_info_contratista(otro)
                    respuesta += formatear_contrato(info_otro, i)
            
            respuesta += "\n═══════════════════════════════════════\n"
            respuesta += "¿En qué más te ayudo?"
            
            return respuesta
        else:
            return f"""❌ No encontré información con la cédula {cedula}.

Verifica que el número esté bien escrito. Si acabas de firmar contrato, puede que tu información aún no esté cargada en el sistema (tarda 24-48 horas).

¿En qué más te puedo ayudar?"""
    
    if intencion in RESPUESTAS:
        return RESPUESTAS[intencion]
    
    return RESPUESTAS['fuera_de_alcance']