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

def obtener_info_completa(cedula):
    """
    Devuelve un dict con la información combinada de contratistas y seguimiento.
    Similar a lo que hace /api/mi-proceso pero en formato texto para el chat.
    """
    from .lector import lector
    registros = lector.buscar_por_cedula(cedula)
    seguimiento = lector_seguimiento.buscar_por_cedula(cedula)
    
    info = {
        'nombre': None,
        'cedula': cedula,
        'estado': None,
        'observacion': None,
        'año': None,
        'pagos': []  # lista de dicts con info de pagos
    }
    
    # Si hay registros en contratistas
    if registros:
        r = registros[0]  # tomamos el primero
        info['nombre'] = r.get('NOMBRE DE CONTRATISTA', 'Sin nombre')
        info['cedula'] = r.get('CEDULA', cedula)
        info['año'] = str(r.get('AÑO', ''))
        estado_original = r.get('ESTADO', 'Sin estado')
        info['estado'] = traducir_estado(estado_original) or f"📋 {estado_original}"
        obs_original = r.get('OBSERVACIÓN', '')
        info['observacion'] = traducir_observacion(obs_original) or (f"📋 {obs_original}" if obs_original else "📋 Sin información adicional")
    
    # Si hay seguimiento, procesar pagos
    if seguimiento:
        solpedidos = {}
        for s in seguimiento:
            solpedido = str(s.get('SOLPEDIDO', 'Desconocido'))
            if solpedido not in solpedidos:
                solpedidos[solpedido] = {
                    'solpedido': solpedido,
                    'nombre': s.get('NOMBRE DEL PROVEEDOR', info['nombre'] or 'Sin nombre'),
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
        
        # Guardar pagos en la info
        for solpedido, data_s in solpedidos.items():
            info['pagos'].append({
                'solpedido': solpedido,
                'pagos': data_s['pagos']
            })
    
    return info

# Links importantes
URL_PORTAL = "https://proveedores.uniminuto.edu"
URL_INSTRUCTIVO = "https://uniminuto.edu/instructivo-proveedores"
URL_FORMATO = "https://uniminuto.edu/formato-ingreso-independientes"

# Contactos
TEL_BOGOTA = "(601) 593 3004"
TEL_NACIONAL = "01 8000 11 93 90"


RESPUESTAS = {

    "saludo": """¡Hola! 👋 Soy tu asistente de contratación de UNIMINUTO Virtual.

Para ver cómo va tu proceso, escribe tu número de cédula.
También te puedo ayudar con:

📋 **Qué documentos enviar**
🌐 **Cómo registrarte en la plataforma**
🔧 **Cómo llenar bien el formulario**
⚠️ **Problemas con el registro** (rechazos, errores)
📝 **Actualizar el RUT** (marca de agua, actividad)
💰 **Estado de tus pagos**
📞 **Si no te contestan o te llamaron**

Escribe tu cédula o tu pregunta para empezar.""",

    "portal_proveedores": f"""🌐 **REGISTRARTE EN LA PLATAFORMA DE PROVEEDORES**

Para registrarte, sigue estos pasos:

1. **Entra a este enlace:** 👉 {URL_PORTAL}
2. **Haz clic en "Registrarse"** (esquina superior derecha).
3. **Llena todos los campos del formulario.** Presta atención a estos puntos clave:

   🏢 **Sede de Operaciones:** debes seleccionar **"Rectoría UNIMINUTO Virtual"**. Es la primera opción. ¡No te equivoques! Si pones otra sede, tu registro será rechazado.

   📦 **Bien o Servicio:** elige **"Servicio"** y luego la categoría que corresponda a tu labor (ej. Educación, Tecnología, etc.).

   👤 **Tratamiento:** selecciona **"Señor(a)"**. **Solo si eres empleado de UNIMINUTO** (colaborador) elige "Empleado(a)".

   📋 **Régimen:**
   - Si eres **Persona Natural** → **Simplificado**
   - Si eres **Empresa / Persona Jurídica** → **Común**

   📧 **Correo electrónico:** debe ser **el mismo que aparece en tu RUT**. Ahí te enviaremos toda la comunicación.

   📮 **Código Postal:** busca el código postal de tu ciudad en Google (ej. "código postal Bogotá").

   💡 **Tip:** Si tienes dudas, descarga el instructivo desde el correo que recibiste o pídemelo.

   **Después de registrarte, envía los documentos requeridos (te los explico más abajo).**""",

    "documentos_natural": """📋 **DOCUMENTOS PARA PERSONA NATURAL**

Todos los documentos deben estar en **PDF, sin contraseña** y con menos de 30 días de expedición.

1. 📄 **Cédula de ciudadanía** (ambas caras).
2. 🏦 **Certificación bancaria** (no mayor a 30 días).
3. 📋 **RUT actualizado** (no mayor a 30 días):
   - Debe decir **"copia"** o **"certificado"** como marca de agua.
   - **NO** debe decir **"en trámite"**.
   - Recomendamos actividad económica **8560** (apoyo a la educación).
4. 📊 **Formato Excel "Ingreso Independientes"** (lo recibiste en el correo).
5. 🏥 **Certificación de ARL** (activa como independiente).
6. 🏥 **Examen médico ocupacional** (vigencia máxima 3 años).

⚠️ Si falta algún documento o no te registras, tu proceso se retrasa y se le notifica a tu supervisor.

📌 **¿Dónde envías esto?** Lo subes en el portal de proveedores, en la sección de "Documentos Adjuntos".

¿Necesitas ayuda con algún documento en específico?""",

    "documentos_juridica": """📋 **DOCUMENTOS PARA EMPRESA / PERSONA JURÍDICA**

Todos los documentos en **PDF, sin contraseña** y con menos de 30 días de expedición.

1. 📄 **Cédula del representante legal**.
2. 🏦 **Certificación bancaria de la empresa** (no mayor a 30 días).
3. 📋 **RUT de la empresa actualizado** (no mayor a 30 días):
   - Marca de agua "copia" o "certificado".
   - No "en trámite".
4. 📑 **Cámara de Comercio** (expedición no mayor a 30 días).
5. 📄 **Cédula del representante legal** (nuevamente, para la plataforma).
6. 🏥 **Certificación de la ARL** de la empresa.
7. 🏥 **Examen médico ocupacional** del representante legal (vigencia 3 años).

⚠️ El correo que registren en la plataforma es donde recibirán toda la comunicación.

¿Necesitas aclarar algún punto?""",

    "documentos_requeridos": """📋 **RESUMEN DE DOCUMENTOS REQUERIDOS**

**Persona Natural:**
- Cédula
- Certificación bancaria (30 días)
- RUT actualizado (30 días, "copia" o "certificado")
- Formato Excel "Ingreso Independientes"
- Certificación ARL
- Examen médico (3 años)

**Persona Jurídica (Empresa):**
- Cédula del representante legal
- Certificación bancaria de la empresa (30 días)
- RUT de la empresa (30 días, "copia" o "certificado")
- Cámara de Comercio (30 días)
- Certificación ARL de la empresa
- Examen médico del representante legal (3 años)

**Todos en PDF y sin contraseña.**

💡 **¿Eres persona natural o empresa?** Dime tu caso y te doy la lista exacta.""",

    "actualizar_rut": """📝 **CÓMO ACTUALIZAR TU RUT**

Tu RUT debe estar **actualizado (menos de 30 días)** y tener una de estas marcas de agua:
✅ **"Copia"**
✅ **"Certificado"**
✅ **"Actualización"**

❌ **NO** debe decir **"En trámite"**.

**Pasos para actualizarlo:**

1. Entra a la página de la DIAN: www.dian.gov.co
2. Inicia sesión con tu usuario y contraseña.
3. Busca la opción **"Actualización RUT"**.
4. Revisa que tus datos estén al día (dirección, correo, actividad económica).
5. **Actividad económica recomendada:** si trabajas en educación, usa el código **8560** (Actividades de apoyo a la educación). Si no, elige la que corresponda a tu labor.
6. Descarga el RUT actualizado en PDF.
7. Verifica que la marca de agua sea la correcta.

⚠️ **Importante:** Si tu RUT dice "en trámite", no sirve. Debes esperar a que la DIAN lo apruebe y luego descargar la versión final.

💡 **Tip:** La actualización la puedes hacer en línea, no necesitas ir a una oficina.""",

    "llenar_plataforma": """🔧 **CÓMO LLENAR BIEN EL FORMULARIO DEL PORTAL**

Cuando estés registrando, presta atención a estos campos CLAVE:

🏢 **Sede de Operaciones:** **Rectoría UNIMINUTO Virtual** (obligatorio).

📦 **Bien o Servicio:** **Servicio** (y luego la categoría correspondiente).

👤 **Tratamiento:** **Señor(a)**. **Solo si eres empleado de UNIMINUTO** → Empleado(a).

📋 **Régimen:**
- Persona Natural → **Simplificado**
- Persona Jurídica → **Común**

👤 **Persona de Contacto:** Pones tus propios datos (el mismo que se está registrando).

📮 **Código Postal:** Busca "código postal [tu ciudad]" en Google.

📧 **Correo:** **Debe ser el mismo que aparece en tu RUT**.

📄 **Objeto Social:** Describe la actividad económica que realizas (ej. "Servicios de consultoría educativa").

💡 **Si te rechazan el registro**, revisa que estos campos estén correctos. La mayoría de los rechazos son por Sede, Régimen o Tratamiento.

¿Tienes duda con algún otro campo? Pregúntame.""",

    "problemas_registro": """⚠️ **PROBLEMAS COMUNES CON EL REGISTRO Y CÓMO SOLUCIONARLOS**

❌ **"Mi registro fue rechazado"** → Puede ser por:

1. **Sede incorrecta:** Debe ser "Rectoría UNIMINUTO Virtual". Si pusiste otra, solicita que rechacen tu registro y vuélvelo a hacer.
2. **Régimen equivocado:** Persona Natural → Simplificado; Empresa → Común.
3. **Tratamiento incorrecto:** Debe ser "Señor(a)" (a menos que seas empleado).
4. **Correo no coincide con RUT:** El correo que pongas debe ser el mismo del RUT.
5. **Documentos con contraseña:** Los PDF no deben tener clave.
6. **RUT en trámite o sin actividad 8560:** Debes actualizarlo.

❌ **"No me deja subir documentos"**
- Asegúrate de que sean PDF y sin contraseña.
- Prueba con Chrome o Firefox actualizados.
- Borra la caché del navegador.

❌ **"No sé qué poner en un campo"**
- Pregúntame el campo específico y te ayudo.

❌ **"Me equivoqué de sede"**
- Solicita el rechazo a Servicios Integrados y vuelve a registrarte en la sede correcta.

Si nada funciona, llama a:
📞 Bogotá: {TEL_BOGOTA}
📞 Nacional: {TEL_NACIONAL}""",

    "estado_pago": """💰 **ESTADO DE TUS PAGOS**

Para saber si ya te pagaron:

1. Revisa en el portal de proveedores el estado de tu factura.
2. Los pagos se hacen según lo pactado en tu contrato:
   - **Pago único:** al finalizar y entregar todo.
   - **Pago mensual:** cada mes según avances.

**Estados que puedes ver:**
- **PTE** = Pendiente (aún no se procesa)
- **LIBERADO** = Listo para pago
- **PAGADO** = Ya te transfirieron

Si tienes dudas con tu pago específico, habla con tu supervisor o con el área financiera.
También puedes preguntarme "¿cómo está mi pago?" y te daré más detalles.""",

    "rechazo_sede": """🏢 **PROBLEMA CON LA SEDE**

La sede que debes seleccionar es **"Rectoría UNIMINUTO Virtual"**.

❌ Si pusiste otra (ej. "Sede Principal", "Cundinamarca", etc.), tu registro será rechazado.

🔧 **Cómo arreglarlo:**
1. Solicita el rechazo de tu registro al área de Servicios Integrados (puedes hacerlo por correo).
2. Una vez rechazado, vuelve a registrarte y selecciona **Rectoría UNIMINUTO Virtual**.
3. Asegúrate de que los demás campos también estén correctos.

💡 **Tip:** La mayoría de los rechazos son por este motivo. Revisa bien antes de enviar.""",

    "rechazo_regimen": """📋 **PROBLEMA CON EL RÉGIMEN**

El régimen que debes seleccionar depende de tu tipo de persona:

✅ **Persona Natural** → **Simplificado**
✅ **Persona Jurídica / Empresa** → **Común**

❌ Si eliges el régimen equivocado, tu registro será rechazado.

🔧 **Cómo arreglarlo:**
1. Solicita el rechazo de tu registro (si ya lo enviaste).
2. Vuelve a registrarte y selecciona el régimen correcto.
3. Verifica también que el tratamiento y la sede estén bien.

💡 **Recuerda:** El régimen debe coincidir con lo que dice tu RUT en el campo "Tipo de contribuyente".""",

    "rechazo_tratamiento": """👤 **PROBLEMA CON EL TRATAMIENTO**

En el campo "Tratamiento" debes seleccionar:

✅ **"Señor(a)"** → Para la mayoría de los casos.
✅ **"Empleado(a)"** → **Solo si eres colaborador de UNIMINUTO** (trabajas en la universidad).

❌ Si pones el que no corresponde, el registro se rechaza.

🔧 **Cómo arreglarlo:**
1. Solicita el rechazo de tu registro.
2. Vuelve a registrarte y elige el tratamiento correcto.

💡 **Duda:** ¿Eres colaborador de UNIMINUTO o externo? Si no estás seguro, pregunta a tu supervisor.""",

    "documentos_con_clave": """🔐 **TUS PDF TIENEN CONTRASEÑA**

Los documentos que subes al portal **no deben tener contraseña**.

🔧 **Cómo quitar la contraseña de un PDF:**

**Opción 1 (Adobe Acrobat):**
- Abre el PDF, ve a "Archivo" → "Propiedades" → "Seguridad" → "Sin seguridad".

**Opción 2 (Imprimir como PDF):**
- Abre el PDF e imprímelo seleccionando "Guardar como PDF" (esto elimina la contraseña).

**Opción 3 (Herramientas online):**
- Usa un servicio gratuito como ilovepdf.com para desbloquear PDFs (asegúrate de que sea seguro).

⚠️ **Importante:** Cuando el documento no tenga contraseña, podrás subirlo sin problema.""",

    "plazo_documentos": """📅 **DOCUMENTOS CON PLAZO DE 30 DÍAS**

Estos documentos deben tener **menos de 30 días de expedición**:

- 🏦 Certificación bancaria
- 📋 RUT
- 📑 Cámara de Comercio (para empresas)

Si tus documentos tienen más de 30 días, **no serán válidos** y tu proceso se retrasará.

🔧 **Qué hacer:**
1. Solicita una nueva certificación bancaria en tu banco.
2. Actualiza tu RUT en la DIAN (puedes hacerlo en línea).
3. Si eres empresa, solicita una copia actualizada de la Cámara de Comercio.

💡 **Consejo:** Mantén estos documentos siempre actualizados para evitar retrasos.""",

    "no_contesta": """📞 **NO TE CONTESTAN O TE LLAMARON Y NO RESPONDISTE**

Es importante que estés atento a las llamadas y correos, ya que el área de contratación puede necesitar comunicarse contigo.

🔧 **Qué hacer si no te contestan:**
- Revisa que tu número de teléfono esté bien escrito en el portal y en el RUT.
- Verifica tu correo electrónico (incluyendo spam).
- Si te llamaron y no pudiste contestar, devuelve la llamada al número que aparezca o contacta a tu supervisor.

📧 **Si no recibes respuesta por correo:**
- Revisa que el correo que registraste sea el correcto.
- Pregunta a tu supervisor si han intentado contactarte.

💡 **Tip:** Si has intentado comunicarte varias veces sin éxito, avisa a tu supervisor para que pueda ayudarte.""",

    "examen_medico": """🏥 **EXAMEN MÉDICO OCUPACIONAL**

El examen médico ocupacional es obligatorio y debe tener **vigencia máxima de 3 años**.

🔧 **¿Dónde lo hago?**
- Puedes realizarlo en cualquier entidad de salud ocupacional (ARL, clínicas, etc.).
- Pide que te entreguen el certificado en formato PDF.

📄 **¿Qué debo entregar?**
- El certificado o resultado del examen, donde se indique que eres apto para el cargo.

⚠️ **Importante:** Si tu examen tiene más de 3 años, debes renovarlo.

💡 **Tip:** Si no sabes dónde hacerlo, consulta con tu ARL o con el área de talento humano de UNIMINUTO.""",

    "certificacion_bancaria": """🏦 **CERTIFICACIÓN BANCARIA**

La certificación bancaria es un documento que expide tu banco donde consta que tienes una cuenta a tu nombre.

🔧 **¿Cómo la obtengo?**
- Solicítala en tu banco (por la app, página web o en una oficina).
- Debe tener **fecha de expedición no mayor a 30 días**.
- Debe estar en **PDF y sin contraseña**.

📄 **¿Qué datos debe tener?**
- Tu nombre completo (igual al RUT).
- Número de cuenta.
- Tipo de cuenta (ahorros/corriente).
- Fecha de expedición.

⚠️ **Importante:** Si tienes cuenta de nómina o de ahorros, ambas sirven, pero asegúrate de que el banco la emita con tu nombre exacto.

💡 **Tip:** Puedes pedirla por la banca en línea, es más rápido.""",

    "cotizacion": """📝 **COTIZACIÓN FIRMADA**

La cotización es un documento donde detallas los servicios que prestarás y los costos.

🔧 **¿Cómo la hago?**
- Usa el formato que te enviaron en el correo (o pídemelo).
- Debe incluir:
  - Tu nombre o razón social.
  - Objeto del contrato (lo que vas a hacer).
  - Valor total (con IVA incluido si aplica).
  - Fecha de elaboración.
- **Debe estar firmada por ti.**

📄 **Formato:** PDF, sin contraseña.

⚠️ **Importante:** La cotización debe coincidir con lo que acordaste con tu supervisor. Si tienes dudas sobre el valor, consulta con él/ella.

💡 **Tip:** Si no tienes el formato, pídemelo y te lo proporciono.""",

    "subir_rut": """📄 **PARA VALIDAR TU RUT, SIGUE ESTOS PASOS:**

1. **Ten listo tu RUT en PDF** (que diga "copia" o "certificado", no "en trámite").
2. **Sube el archivo** usando el botón de abajo.
3. **Espera el análisis** - te diré qué está bien y qué falta.

📋 **Lo que voy a verificar:**
- ✅ Que diga "copia" o "certificado" (no "en trámite").
- ✅ Que tenga la actividad 8560 (o alguna relacionada con educación).
- ✅ Que tenga menos de 30 días de expedición.
- ✅ Que la cédula coincida con la tuya.

⚠️ **Importante:** Por ahora solo funciona con PDFs digitales (no escaneados como imagen).

📎 **Botón para subir:** (debes ir a "Mi Proceso" para subirlo).""",

    "fuera_de_alcance": """Disculpa, no entendí bien tu pregunta.

Puedo ayudarte con estos temas:
📋 **Documentos que debes enviar** (persona natural o empresa).
🌐 **Cómo registrarte en el portal** (paso a paso).
🔧 **Cómo llenar bien el formulario** (campos clave).
⚠️ **Problemas con el registro** (rechazos, errores).
📝 **Actualizar el RUT** (marca de agua, actividad).
💰 **Estado de tus pagos**.
📞 **Si no te contestan o te llamaron**.

Escribe tu cédula para ver el estado de tu proceso, o cuéntame en qué te ayudo.
Puedes usar palabras clave como "rechazo", "sede", "régimen", "contraseña", etc.""",
}

# Las funciones auxiliares (extraer_cedula, detectar_intencion, etc.) se mantienen igual,
# pero asegúrate de que detectar_intencion incluya las nuevas etiquetas.
# También se debe actualizar la función responder_contratista para manejar las nuevas intenciones.

def extraer_cedula(texto):
    matches = re.findall(r'\b\d{6,12}\b', texto)
    for m in matches:
        if len(m) >= 7:
            return m
        if len(m) >= 6 and not m.startswith('20'):
            return m
    return None

def detectar_intencion(texto):
    t = texto.lower()
    cedula = extraer_cedula(texto)
    
    # Detectar intención de subir/revisar el RUT.
    _verbos_accion_rut = ['subir', 'revisar', 'validar', 'verificar', 'analizar', 'cargar', 'adjuntar', 'enviar', 'mandar']
    if 'rut' in t and any(v in t for v in _verbos_accion_rut):
        return 'subir_rut', cedula

    # Cédula tiene prioridad
    if cedula:
        return 'consulta_estado', cedula
    
    # Saludos
    if any(p in t for p in ['hola', 'buenos', 'buenas', 'hi', 'hello', 'ayuda']):
        return 'saludo', cedula
    
    # Rechazos específicos (van antes de problemas_registro para ser más precisos)
    if any(p in t for p in ['sede', 'rectoría', 'sede operaciones']) and ('rechaz' in t or 'equivoc' in t or 'mal' in t):
        return 'rechazo_sede', cedula
    if 'regimen' in t and ('rechaz' in t or 'equivoc' in t or 'mal' in t):
        return 'rechazo_regimen', cedula
    if 'tratamiento' in t and ('rechaz' in t or 'equivoc' in t or 'mal' in t):
        return 'rechazo_tratamiento', cedula
    if 'contraseña' in t or 'clave' in t or 'pdf con clave' in t:
        return 'documentos_con_clave', cedula
    if '30 días' in t or '30 dias' in t or 'vencido' in t or 'vigencia' in t:
        return 'plazo_documentos', cedula
    if 'no contesta' in t or 'no responden' in t or 'llamada' in t:
        return 'no_contesta', cedula
    if 'examen médico' in t or 'examen ocupacional' in t:
        return 'examen_medico', cedula
    if 'certificación bancaria' in t or 'certificacion bancaria' in t:
        return 'certificacion_bancaria', cedula
    if 'cotización' in t or 'cotizacion' in t:
        return 'cotizacion', cedula
    
    # Llenar plataforma
    if any(p in t for p in ['llenar', 'como lleno', 'campos', 'persona de contacto', 'codigo ciiu', 'objeto social', 'codigo postal', 'regimen', 'tratamiento', 'sede operaciones', 'bien o servicio']):
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
    if any(p in t for p in ['problema', 'no puedo', 'error', 'no me deja', 'rechazo', 'rechazado', 'no funciona', 'rechaz']):
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

    # Clasificador semántico para frases no cubiertas
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

1. **Ten listo tu RUT en PDF** (que diga "copia" o "certificado", no "en trámite").
2. **Sube el archivo** usando el botón de abajo (en "Mi Proceso").
3. **Espera el análisis** - te diré qué está bien y qué falta.

📋 **Lo que voy a verificar:**
- ✅ Que diga "copia" o "certificado" (no "en trámite").
- ✅ Que tenga la actividad 8560 (o alguna relacionada con educación).
- ✅ Que tenga menos de 30 días de expedición.
- ✅ Que la cédula coincida con la tuya.

⚠️ **Importante:** Por ahora solo funciona con PDFs digitales (no escaneados como imagen).

📎 [Selecciona tu RUT en PDF para subirlo]"""
    
    # Si tiene cédula, buscar al contratista
    if cedula:
        registros = lector.buscar_por_cedula(cedula)
        
        if registros:
            info_principal = lector.obtener_info_contratista(registros[0])
            
            respuesta = f"""📋 **ESTADO DE TU PROCESO**

👤 **Nombre:** {info_principal['nombre']}
🆔 **Cédula:** {info_principal['cedula']}
📅 **Año:** {info_principal['año']}

═══════════════════════════════════════
"""
            respuesta += formatear_contrato(info_principal)
            
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
    
    # Respuestas para intenciones específicas
    if intencion in RESPUESTAS:
        return RESPUESTAS[intencion]
    
    return RESPUESTAS['fuera_de_alcance']