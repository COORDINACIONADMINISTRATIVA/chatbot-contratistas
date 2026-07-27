"""
Chatbot para contratistas - Versión Final con PRIORIDAD RUT
"""
import re
import random
from .lector import lector
from .interprete import traducir_observacion, traducir_estado

# ============================================================
# IMPORTS DEL SISTEMA DE CONOCIMIENTO
# ============================================================
from chatbot.conocimiento.rut import PATRONES_RUT, respuesta_rut
from chatbot.conocimiento.documentos import PATRONES_DOCUMENTOS, respuesta_documentos
from chatbot.conocimiento.portal import PATRONES_PORTAL, respuesta_portal
from chatbot.conocimiento.contratos import PATRONES_CONTRATOS, respuesta_contratos
from chatbot.memoria import memoria
from chatbot.respuestas_campos import RESPUESTAS_CAMPOS

_clasificador_semantico = None


def _obtener_clasificador():
    global _clasificador_semantico
    if _clasificador_semantico is None:
        from nlp.embedding_classifier import EmbeddingClassifier
        _clasificador_semantico = EmbeddingClassifier()
        _clasificador_semantico.cargar_modelo()
    return _clasificador_semantico


def obtener_info_completa(cedula):
    from .lector import lector
    from contratacion.lector_seguimiento import lector_seguimiento
    registros = lector.buscar_por_cedula(cedula)
    seguimiento = lector_seguimiento.buscar_por_cedula(cedula)
    
    info = {
        'nombre': None,
        'cedula': cedula,
        'estado': None,
        'observacion': None,
        'año': None,
        'pagos': []
    }
    
    if registros:
        r = registros[0]
        info['nombre'] = r.get('NOMBRE DE CONTRATISTA', 'Sin nombre')
        info['cedula'] = r.get('CEDULA', cedula)
        info['año'] = str(r.get('AÑO', ''))
        estado_original = r.get('ESTADO', 'Sin estado')
        info['estado'] = traducir_estado(estado_original) or f"📋 {estado_original}"
        obs_original = r.get('OBSERVACIÓN', '')
        info['observacion'] = traducir_observacion(obs_original) or (f"📋 {obs_original}" if obs_original else "📋 Sin información adicional")
    
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
        
        for solpedido, data_s in solpedidos.items():
            info['pagos'].append({
                'solpedido': solpedido,
                'pagos': data_s['pagos']
            })
    
    return info


URL_PORTAL = "https://proveedores.uniminuto.edu"
URL_INSTRUCTIVO = "https://uniminuto.edu/instructivo-proveedores"
URL_FORMATO = "https://uniminuto.edu/formato-ingreso-independientes"


# ============================================================
# RESPUESTAS MÚLTIPLES (COMPLETAS)
# ============================================================

RESPUESTAS = {

    # ==================== SALUDO ====================
    "saludo": [
        """¡Bienvenido! 👋 Soy el asistente de apoyo en contratación de UNIMINUTO Virtual.

Estoy aquí para ayudarle con todo el proceso de contratación. Puedo orientarle sobre:

📋 Documentos que debe enviar según su tipo de contratación (persona natural o empresa).
🌐 Cómo registrarse en el portal de proveedores de UNIMINUTO.
🔧 Cómo diligenciar correctamente el formulario de registro.
⚠️ Problemas comunes con el registro y cómo solucionarlos.
📝 Actualización del RUT, marcas de agua y actividad económica recomendada.

Para conocer el estado de su proceso, simplemente escriba su número de cédula.
¿En qué puedo ayudarle hoy?""",
        """Hola, soy el asistente virtual de contratación de UNIMINUTO Virtual. 😊

Estoy diseñado para resolver sus dudas sobre el proceso de contratación. Estos son los temas que manejo:

📋 Documentos requeridos (persona natural y empresa).
🌐 Registro en el portal de proveedores.
🔧 Diligenciamiento del formulario.
⚠️ Solución de problemas y rechazos.
📝 Actualización del RUT.

Para consultar su estado, solo escriba su número de cédula.
¿Cómo puedo ayudarle el día de hoy?""",
        """¡Buen día! 👋 Le saluda el asistente de contratación de UNIMINUTO Virtual.

Mi objetivo es facilitarle todo el proceso de contratación, desde el registro hasta la entrega de documentos. 

Puedo ayudarle con:
- Documentos que debe presentar.
- Pasos para registrarse en el portal.
- Problemas comunes y cómo solucionarlos.
- Actualización de su RUT.

¿En qué tema específico necesita apoyo?"""
    ],

    # ==================== CREAR RUT ====================
    "crear_rut": [
        """📝 CÓMO OBTENER SU RUT POR PRIMERA VEZ - GUÍA COMPLETA

Si nunca ha tenido RUT o necesita obtenerlo por primera vez, siga estos pasos:

🔹 ¿QUÉ ES EL RUT?
El RUT (Registro Único Tributario) es el documento que identifica a las personas y empresas ante la DIAN para efectos tributarios.

🔹 ¿QUIÉN DEBE TENER RUT?
- Personas naturales que prestan servicios (como contratistas).
- Personas jurídicas (empresas).
- Cualquier persona que realice actividades económicas.

🔹 PASOS PARA OBTENERLO:

📌 PASO 1: INGRESE A LA PÁGINA DE LA DIAN
- Entre a: www.dian.gov.co
- Busque la opción "Registro Único Tributario - RUT".

📌 PASO 2: COMPLETE EL FORMULARIO
- Diligencie sus datos personales: nombre, cédula, dirección, teléfono, correo.
- Indique su actividad económica principal.
- Actividad recomendada para contratistas: código 8560 (Actividades de apoyo a la educación).

📌 PASO 3: SELECCIONE EL RÉGIMEN
- Si es persona natural sin empresa → "Simplificado".
- Si es persona jurídica o empresa → "Común".

📌 PASO 4: DESCARGUE SU RUT
- Una vez completado, el sistema le generará un archivo PDF.
- Verifique que tenga la marca de agua "copia" o "certificado".

📌 PASO 5: GUARDE EL DOCUMENTO
- Guárdelo en PDF y sin contraseña.
- Verifique que la cédula esté correcta.

⚠️ IMPORTANTE:
- La fecha de expedición debe ser menor a 30 días para el proceso de contratación.
- La actividad económica debe coincidir con la labor que va a realizar.

💡 CONSEJO:
- Si tiene dudas, busque tutoriales en YouTube: "Cómo obtener RUT en la DIAN".
- También puede ir a una oficina de la DIAN para asesoría presencial.

¿Necesita ayuda con algún paso en particular?""",
        """📝 GUÍA RÁPIDA PARA OBTENER SU RUT

Si no tiene RUT y necesita crearlo:

1. Ingrese a www.dian.gov.co
2. Busque "Registro Único Tributario"
3. Complete el formulario con sus datos personales
4. Seleccione el régimen que le corresponde (Simplificado o Común)
5. Descargue el PDF con la marca de agua "copia" o "certificado"

💡 Actividad recomendada: 8560 (apoyo a la educación)

¿Tiene dudas sobre cómo llenar el formulario?"""
    ],

    # ==================== ACTUALIZAR RUT ====================
    "actualizar_rut": [
        """📝 CÓMO ACTUALIZAR SU RUT

El RUT debe estar actualizado (menos de 30 días) y tener una de estas marcas de agua:
✅ "Copia"
✅ "Certificado"
✅ "Actualización"

❌ NO debe decir "En trámite".

🔧 PASOS PARA ACTUALIZARLO:

1. Ingrese a la página de la DIAN: www.dian.gov.co
2. Inicie sesión con su usuario y contraseña.
3. Busque la opción "Actualización RUT".
4. Revise que sus datos estén al día (dirección, correo, actividad económica).
5. Actividad económica recomendada: código 8560 (apoyo a la educación), pero puede tener otra.
6. Descargue el RUT actualizado en PDF.
7. Verifique que la marca de agua sea la correcta.

⚠️ Si su RUT dice "en trámite", no sirve. Debe esperar a que la DIAN lo apruebe.

💡 La actualización la puede hacer en línea, no necesita ir a una oficina.

¿Necesita ayuda con algún paso en particular?""",
        """📝 ACTUALIZACIÓN DEL RUT

Para actualizar su RUT, siga estos pasos:

1. Ingrese a www.dian.gov.co
2. Inicie sesión con su usuario y contraseña.
3. Busque "Actualización RUT" en el menú.
4. Revise y actualice sus datos personales y actividad económica.
5. Descargue el RUT con marca de agua "copia" o "certificado".
6. Verifique que la fecha sea reciente (menos de 30 días).

Recuerde: la actividad 8560 (apoyo a la educación) es la recomendada, pero puede tener otra.

¿Tiene dudas sobre cómo hacerlo en la DIAN?"""
    ],

    # ==================== SUBIR RUT ====================
    "subir_rut": [
        """📄 PARA VALIDAR SU RUT, SIGA ESTOS PASOS:

1. Tenga listo su RUT en PDF:
   - Debe decir "copia" o "certificado" (no "en trámite").
   - Menos de 30 días de expedición.

2. Vaya a la sección "Validador de RUT" en "Consultar mi estado".

3. Suba el archivo:
   - Haga clic en "Seleccionar RUT (PDF)".
   - O arrastre y suelte el archivo.

4. Espere el análisis:
   - Le diré qué está bien y qué necesita corregir.

📋 LO QUE VOY A VERIFICAR:
- ✅ Marca de agua: "copia" o "certificado" (NO "en trámite").
- ✅ Actividad económica 8560 o relacionada con educación (recomendado).
- ✅ Fecha de expedición: menos de 30 días.
- ✅ Cédula: debe coincidir con la suya.

⚠️ Por ahora solo funciona con PDFs digitales.

¿Ya tiene listo su RUT?""",
        """📄 VALIDACIÓN DE RUT

Para validar su RUT:
1. Tenga el PDF listo ("copia" o "certificado", no "en trámite").
2. Suba el archivo en la sección "Validador de RUT".
3. Espere el análisis automático.

El sistema verificará la marca de agua, actividad económica, fecha y cédula.

¿Tiene su RUT en PDF listo para subir?"""
    ],

    # ==================== QUÉ ES EL RUT ====================
    "que_es_rut": [
        """📋 ¿QUÉ ES EL RUT?

El RUT (Registro Único Tributario) es el documento oficial que identifica a una persona natural o jurídica ante la DIAN (Dirección de Impuestos y Aduanas Nacionales) de Colombia.

🔹 ¿PARA QUÉ SIRVE?
- Identifica su obligación tributaria ante el Estado colombiano.
- Le permite emitir facturas y documentos con validez legal.
- Es un requisito indispensable para contratar con entidades como UNIMINUTO.
- Permite a la DIAN conocer su actividad económica y ubicación.

🔹 ¿QUIÉN DEBE TENERLO?
- Toda persona natural que ejerza una actividad económica, así sea ocasional.
- Todas las empresas, sociedades y personas jurídicas.
- Contratistas independientes que prestan servicios a entidades como UNIMINUTO.
- Profesionales que emiten facturas por sus servicios (abogados, ingenieros, consultores, etc.).

🔹 ¿DÓNDE LO OBTIENEN?
- Exclusivamente en la página oficial de la DIAN: www.dian.gov.co
- Debe crear un usuario en la plataforma y seguir el proceso de registro.
- También puede hacerlo en las oficinas de la DIAN, pero con cita previa.

🔹 ¿ES OBLIGATORIO?
Sí. Para cualquier proceso de contratación con UNIMINUTO, el RUT es un documento obligatorio e indispensable. Sin RUT, no se puede formalizar el contrato.

⚠️ IMPORTANTE:
Para contratar con UNIMINUTO Virtual, su RUT debe cumplir con estos requisitos:
- Estar actualizado (fecha de expedición menor a 30 días).
- Tener marca de agua "Copia" o "Certificado".
- No debe decir "En trámite" ni "Borrador".
- La actividad económica debe ser coherente con la labor que va a desempeñar.

¿Necesita más información sobre algún aspecto específico del RUT?"""
    ],

    # ==================== PROCESO DE CONTRATACIÓN ====================
    "proceso_contratacion": [
        """📋 PROCESO DE CONTRATACIÓN EN UNIMINUTO VIRTUAL - GUÍA COMPLETA

El proceso de contratación consta de varias etapas que debe seguir cuidadosamente. Aquí le explico cada una:

🔹 ETAPA 1: REGISTRO EN EL PORTAL DE PROVEEDORES
Debe ingresar al portal de proveedores (https://proveedores.uniminuto.edu) y crear su cuenta como proveedor.
Es importante que seleccione "Rectoría UNIMINUTO Virtual" como sede de operaciones.
El régimen y tratamiento deben ser correctos según su tipo de persona (natural o jurídica).
Si tiene dudas sobre cómo hacerlo, puedo explicarle paso a paso.

🔹 ETAPA 2: ENTREGA DE DOCUMENTOS
Una vez registrado, debe subir los documentos requeridos en formato PDF y sin contraseña.
Los documentos varían según sea persona natural o empresa.
Todos los documentos deben tener menos de 30 días de expedición (excepto el examen médico).
Puedo darle la lista exacta según su caso.

🔹 ETAPA 3: VALIDACIÓN DE DOCUMENTOS
El área de contratación revisará sus documentos y verificará que cumplan con los requisitos.
Si todo está correcto, su proceso avanza a la siguiente etapa.
Si hay algún problema, se le notificará para que lo corrija.

🔹 ETAPA 4: FIRMA DE CONTRATO
Una vez validados los documentos, se genera el contrato para su firma.
Usted recibirá un correo con las instrucciones para firmar digitalmente.
Es importante que firme dentro de los plazos establecidos.

🔹 ETAPA 5: INICIO DE LABORES
Después de firmar el contrato, se formaliza su vinculación y puede comenzar a prestar sus servicios.
Su supervisor le indicará las fechas y actividades específicas.

📌 RECOMENDACIONES IMPORTANTES:
- Revise constantemente su correo electrónico (incluyendo spam).
- Mantenga sus documentos actualizados.
- Responda oportunamente las comunicaciones del área de contratación.
- Si tiene dudas, no dude en preguntarme.

¿En qué etapa del proceso se encuentra actualmente?""",
        """📌 GUÍA DEL PROCESO DE CONTRATACIÓN EN UNIMINUTO VIRTUAL

Para que su proceso sea exitoso, debe seguir estos pasos en orden:

1. REGISTRO EN PORTAL DE PROVEEDORES
   - Ingrese a https://proveedores.uniminuto.edu
   - Cree su cuenta como proveedor.
   - Seleccione "Rectoría UNIMINUTO Virtual" como sede.
   - Elija el régimen y tratamiento correctos según su tipo de persona.

2. ENVÍO DE DOCUMENTOS
   - Prepare todos los documentos en PDF y sin contraseña.
   - Revise que tengan menos de 30 días de expedición.
   - Suba los documentos en el portal, en la sección correspondiente.
   - Si es persona natural, necesita: cédula, certificación bancaria, RUT actualizado, formato Excel, certificación ARL y examen médico.
   - Si es empresa: cédula del representante, certificación bancaria, RUT de la empresa, Cámara de Comercio, ARL y examen médico.

3. VALIDACIÓN
   - El equipo de contratación revisará sus documentos.
   - Si están correctos, su proceso continúa.
   - Si hay errores, se le notificará para que los corrija.

4. FIRMA DEL CONTRATO
   - Recibirá un correo con el contrato para firmar.
   - Firme digitalmente dentro del plazo indicado.

5. INICIO DE ACTIVIDADES
   - Una vez firmado, podrá comenzar a prestar sus servicios.
   - Su supervisor le dará las instrucciones específicas.

⚠️ ADVERTENCIA:
El no cumplir con alguno de estos pasos puede generar retrasos en su proceso.
Si tiene dudas en cualquier etapa, pregúnteme y le ayudo.

¿Ya realizó alguno de estos pasos?"""
    ],

    # ==================== PORTAL PROVEEDORES ====================
    "portal_proveedores": [
        f"""🌐 REGISTRO EN EL PORTAL DE PROVEEDORES - PASO A PASO

A continuación, le explico detalladamente cómo registrarse en el portal de proveedores de UNIMINUTO:

📌 PASO 1: ACCEDER AL PORTAL
Ingrese al siguiente enlace: 👉 {URL_PORTAL}

📌 PASO 2: INICIAR EL REGISTRO
Haga clic en el botón "Registrarse" en la esquina superior derecha.

📌 PASO 3: DILIGENCIAR EL FORMULARIO
Complete todos los campos del formulario con atención:

🏢 SEDE DE OPERACIONES: "Rectoría UNIMINUTO Virtual" (primera opción).
📦 BIEN O SERVICIO: "Servicio" + categoría correspondiente.
👤 TRATAMIENTO: "Señor(a)" (o "Empleado(a)" si es colaborador).
📋 RÉGIMEN: "Simplificado" (natural) o "Común" (empresa).
📧 CORREO: El mismo que aparece en su RUT.
📮 CÓDIGO POSTAL: Busque el de su ciudad en Google.

📌 PASO 4: ENVIAR EL REGISTRO
Revise toda la información y haga clic en "Enviar" o "Registrar".

📌 PASO 5: ESPERAR LA VALIDACIÓN
El sistema validará su información y recibirá un correo de confirmación si todo está correcto.

💡 CONSEJOS IMPORTANTES:
- Si tiene dudas, descargue el instructivo desde el correo que recibió.
- Después de registrarse, debe enviar los documentos requeridos.
- Si su registro es rechazado, puede corregir y volver a intentarlo.

¿Necesita ayuda con algún campo en específico?""",
        f"""🌐 REGISTRO EN LA PLATAFORMA DE PROVEEDORES

Para completar su registro correctamente, siga estas indicaciones:

1. Ingrese a {URL_PORTAL}
2. Seleccione "Registrarse"
3. Diligencie los campos con atención:
   - Sede: "Rectoría UNIMINUTO Virtual"
   - Bien o Servicio: "Servicio"
   - Tratamiento: "Señor(a)" o "Empleado(a)"
   - Régimen: "Simplificado" o "Común"
   - Correo: igual al de su RUT
   - Código Postal: busque el de su ciudad

4. Revise todo antes de enviar.

Recuerde que después del registro debe enviar los documentos que le solicitaron.

¿Tiene alguna duda sobre algún campo en particular?"""
    ],

    # ==================== PROBLEMAS PORTAL ====================
    "problemas_portal": [
        """⚠️ PROBLEMAS CON EL PORTAL - SOLUCIONES

Aquí le explico los problemas más frecuentes y cómo solucionarlos:

🔹 PROBLEMA 1: "NO CARGA LA PÁGINA"
- Causa: Puede ser problema de internet o del navegador.
- Solución:
  1. Verifique su conexión a internet.
  2. Pruebe con otro navegador (Chrome, Firefox, Edge).
  3. Limpie la caché del navegador.
  4. Intente en otro horario (evite horas pico).

🔹 PROBLEMA 2: "ERROR AL REGISTRARSE"
- Causa: Algún campo está mal diligenciado.
- Solución:
  1. Revise que todos los campos estén completos.
  2. Verifique la sede: debe ser "Rectoría UNIMINUTO Virtual".
  3. Verifique el régimen y tratamiento.
  4. Asegúrese de que el correo sea el mismo del RUT.

🔹 PROBLEMA 3: "NO RECUERDO MI CONTRASEÑA"
- Solución:
  1. Vaya a la página de inicio de sesión.
  2. Haga clic en "¿Olvidó su contraseña?".
  3. Siga las instrucciones para recuperarla.

🔹 PROBLEMA 4: "NO ME LLEGA EL CORREO DE CONFIRMACIÓN"
- Solución:
  1. Revise la carpeta de spam o correo no deseado.
  2. Verifique que el correo registrado sea correcto.
  3. Espere al menos 24 horas.

🔹 PROBLEMA 5: "SE QUEDA CARGANDO"
- Solución:
  1. Recargue la página (F5).
  2. Use la opción "Ventana de incógnito" en Chrome.
  3. Verifique su conexión a internet.

💡 SI NADA FUNCIONA:
- Comuníquese con su supervisor.
- Contacte al área de contratación de UNIMINUTO Virtual.

¿Qué problema específico está teniendo con el portal?"""
    ],

    # ==================== LLENAR PLATAFORMA ====================
    "llenar_plataforma": [
        """🔧 CÓMO LLENAR CORRECTAMENTE EL FORMULARIO DEL PORTAL

Presta atención a estos campos CLAVE para evitar rechazos:

🏢 SEDE DE OPERACIONES:
Debe seleccionar "Rectoría UNIMINUTO Virtual". Es la primera opción.

📦 BIEN O SERVICIO:
Seleccione "Servicio" y luego la categoría que corresponda a su labor.

👤 TRATAMIENTO:
- "Señor(a)" → si es persona natural/independiente.
- "Empleado(a)" → solo si es colaborador de UNIMINUTO.

📋 RÉGIMEN:
- Persona Natural → "Simplificado".
- Empresa → "Común".

📧 CORREO ELECTRÓNICO:
Debe ser el mismo que aparece en su RUT.

📮 CÓDIGO POSTAL:
Busque el código postal de su ciudad en Google.

💡 La mayoría de los rechazos son por Sede, Régimen o Tratamiento.

¿Tiene duda con algún campo específico?""",
        """🔧 DILIGENCIAMIENTO DEL FORMULARIO

Para evitar errores en su registro, verifique estos campos:

1. Sede de Operaciones: "Rectoría UNIMINUTO Virtual"
2. Bien o Servicio: "Servicio" + categoría
3. Tratamiento: "Señor(a)" o "Empleado(a)"
4. Régimen: "Simplificado" (natural) o "Común" (empresa)
5. Correo: igual al de su RUT
6. Código Postal: busque el de su ciudad

Revise todo antes de enviar para evitar rechazos.

¿En qué campo necesita ayuda?"""
    ],

    # ==================== DOCUMENTOS NATURAL ====================
    "documentos_natural": [
        """📋 DOCUMENTOS PARA PERSONA NATURAL (CONTRATISTA INDEPENDIENTE)

A continuación, la lista detallada de documentos que debe presentar:

📄 1. CÉDULA DE CIUDADANÍA (AMBAS CARAS)
   - Escanee ambas caras y unifíquelas en un solo PDF.
   - Asegúrese de que se vean claramente todos los datos.

🏦 2. CERTIFICACIÓN BANCARIA
   - Fecha de expedición NO mayor a 30 días.
   - Debe estar a su nombre (igual al RUT).
   - Solicítela en su banco (app, web o sucursal).

📋 3. RUT ACTUALIZADO
   - Fecha de expedición NO mayor a 30 días.
   - Marca de agua: "copia" o "certificado" (NO "en trámite").
   - Actividad económica: recomendada 8560, pero puede tener otra.

📊 4. FORMATO EXCEL "INGRESO INDEPENDIENTES"
   - Diligéncielo completamente.
   - Guárdelo con su nombre y cédula.

🏥 5. CERTIFICACIÓN DE ARL
   - Activa como trabajador independiente.
   - Certificación reciente.

🏥 6. EXAMEN MÉDICO OCUPACIONAL
   - Vigencia máxima de 3 años.
   - Debe indicar que es APTO para el cargo.

⚠️ TODOS los documentos deben estar en PDF y sin contraseña.

¿Necesita ayuda con algún documento en específico?""",
        """📋 REQUISITOS PARA PERSONA NATURAL

Para completar su proceso de contratación, debe presentar estos documentos:

1. Cédula de ciudadanía (ambas caras, PDF)
2. Certificación bancaria (máx. 30 días, PDF)
3. RUT actualizado (máx. 30 días, "copia" o "certificado")
4. Formato Excel "Ingreso Independientes"
5. Certificación ARL activa
6. Examen médico ocupacional (máx. 3 años)

Todos deben estar en PDF y sin contraseña.

¿Cuál de estos documentos necesita ayuda para obtener?"""
    ],

    # ==================== DOCUMENTOS JURÍDICA ====================
    "documentos_juridica": [
        """📋 DOCUMENTOS PARA EMPRESA / PERSONA JURÍDICA

Lista detallada de documentos para empresas:

📄 1. CÉDULA DEL REPRESENTANTE LEGAL (AMBAS CARAS)
   - Escanee ambas caras en un solo PDF.

🏦 2. CERTIFICACIÓN BANCARIA DE LA EMPRESA
   - Fecha de expedición NO mayor a 30 días.
   - A nombre de la empresa (igual al RUT).

📋 3. RUT DE LA EMPRESA ACTUALIZADO
   - Fecha de expedición NO mayor a 30 días.
   - Marca de agua: "copia" o "certificado".

📑 4. CÁMARA DE COMERCIO
   - Fecha de expedición NO mayor a 30 días.
   - Certificado de existencia y representación legal.

📄 5. CÉDULA DEL REPRESENTANTE LEGAL (nuevamente)
   - Algunas secciones del portal la solicitan otra vez.

🏥 6. CERTIFICACIÓN DE LA ARL DE LA EMPRESA
   - Activa y al día.

🏥 7. EXAMEN MÉDICO OCUPACIONAL
   - Del representante legal.
   - Vigencia máxima de 3 años.

⚠️ TODOS los documentos en PDF y sin contraseña.

¿Necesita ayuda con algún documento en específico?""",
        """📋 DOCUMENTOS PARA PERSONA JURÍDICA

Para empresas, los documentos requeridos son:

1. Cédula del representante legal (ambas caras)
2. Certificación bancaria de la empresa (máx. 30 días)
3. RUT de la empresa actualizado (máx. 30 días)
4. Cámara de Comercio (máx. 30 días)
5. Cédula del representante legal (nuevamente)
6. Certificación ARL de la empresa
7. Examen médico del representante legal (máx. 3 años)

Todos deben estar en PDF y sin contraseña.

¿Tiene todos estos documentos listos?"""
    ],

    # ==================== DOCUMENTOS REQUERIDOS ====================
    "documentos_requeridos": [
        """📋 RESUMEN DE DOCUMENTOS REQUERIDOS

Según su tipo de contratación, estos son los documentos que debe presentar:

📌 PERSONA NATURAL (INDEPENDIENTE):
1. Cédula de ciudadanía (ambas caras).
2. Certificación bancaria (máx. 30 días).
3. RUT actualizado (máx. 30 días, "copia" o "certificado").
4. Formato Excel "Ingreso Independientes".
5. Certificación ARL activa.
6. Examen médico ocupacional (máx. 3 años).

📌 PERSONA JURÍDICA (EMPRESA):
1. Cédula del representante legal (ambas caras).
2. Certificación bancaria de la empresa (máx. 30 días).
3. RUT de la empresa actualizado (máx. 30 días).
4. Cámara de Comercio (máx. 30 días).
5. Cédula del representante legal (nuevamente).
6. Certificación ARL de la empresa.
7. Examen médico del representante legal (máx. 3 años).

📌 REQUISITOS GENERALES:
- Todos en PDF.
- Sin contraseña.
- Fecha de expedición NO mayor a 30 días (excepto examen médico).

¿Es persona natural o empresa? Dígame y le doy la lista exacta.""",
        """📋 DOCUMENTOS QUE DEBE PRESENTAR

El tipo de documentos que necesita depende de su condición:

Si es PERSONA NATURAL:
- Cédula
- Certificación bancaria
- RUT actualizado
- Formato Excel
- ARL
- Examen médico

Si es EMPRESA:
- Cédula del representante
- Certificación bancaria de la empresa
- RUT de la empresa
- Cámara de Comercio
- ARL de la empresa
- Examen médico del representante

¿Me confirma si es persona natural o empresa?"""
    ],

    # ==================== EXAMEN MÉDICO ====================
    "examen_medico": [
        """🏥 EXAMEN MÉDICO OCUPACIONAL

El examen médico ocupacional es obligatorio y debe tener vigencia máxima de 3 años.

🔧 ¿DÓNDE LO HAGO?
- Puede realizarlo en cualquier entidad de salud ocupacional (ARL, clínicas, etc.).
- Pida que le entreguen el certificado en formato PDF.

📄 ¿QUÉ DEBO ENTREGAR?
- El certificado o resultado del examen.
- Debe indicar que es APTO para el cargo.

⚠️ IMPORTANTE:
- Si su examen tiene más de 3 años, debe renovarlo.
- El examen es obligatorio, no puede omitirlo.

💡 Si no sabe dónde hacerlo, consulte con su ARL o con el área de talento humano de UNIMINUTO.

¿Necesita ayuda para encontrar dónde hacer su examen?""",
        """🏥 EXAMEN MÉDICO

El examen médico ocupacional debe tener vigencia máxima de 3 años.

Puede realizarlo en:
- ARL (Administradora de Riesgos Laborales)
- Clínicas ocupacionales
- IPS autorizadas

Solicite el certificado en formato PDF, indicando que es APTO para el cargo.

¿Ya tiene su examen médico al día?"""
    ],

    # ==================== ARL ====================
    "arl": [
        """🏥 CERTIFICACIÓN DE ARL - GUÍA COMPLETA

🔹 ¿QUÉ ES LA ARL?
La ARL (Administradora de Riesgos Laborales) es la entidad que protege a los trabajadores contra accidentes y enfermedades relacionadas con su trabajo.

🔹 ¿ES OBLIGATORIA?
Sí. Todos los contratistas que prestan servicios a UNIMINUTO deben tener ARL activa.

🔹 ¿QUÉ DEBO ENTREGAR?
- Certificación de afiliación a ARL.
- Debe estar activa como trabajador independiente (o como empresa).
- Debe ser reciente.

🔹 ¿CÓMO OBTENGO LA CERTIFICACIÓN?
1. Comuníquese con su ARL.
2. Solicite la certificación de afiliación.
3. Indique que la necesita para contratar con UNIMINUTO.
4. Solicítela en formato PDF (sin contraseña).

🔹 ARL RECOMENDADAS:
- Positiva
- Sura
- Colmena
- AXA Colpatria
- Seguros Bolívar
- La Equidad

🔹 ¿QUÉ PASA SI NO TENGO ARL?
- No puede contratar con UNIMINUTO.
- Debe afiliarse antes de iniciar el proceso.

💡 CONSEJO:
Si no tiene ARL, comuníquese con una de las ARL recomendadas y solicite su afiliación como trabajador independiente.

¿Ya tiene ARL o necesita ayuda para afiliarse?""",
        """🏥 ARL - INFORMACIÓN RÁPIDA

La ARL es obligatoria para todo contratista de UNIMINUTO Virtual.

🔹 ¿CÓMO OBTENERLA?
1. Elija una ARL (Positiva, Sura, Colmena, etc.)
2. Solicite afiliación como trabajador independiente
3. Reciba la certificación en PDF

🔹 ¿CUÁNTO CUESTA?
- El costo varía según la ARL y el tipo de afiliación.
- Consulte directamente con la ARL de su elección.

¿Necesita ayuda para afiliarse a una ARL?"""
    ],

    # ==================== FIRMA DE CONTRATO ====================
    "firma_contrato": [
        """📝 CÓMO FIRMAR EL CONTRATO DIGITALMENTE

El proceso de firma de contrato en UNIMINUTO Virtual se realiza de forma digital. Aquí le explico cómo hacerlo:

🔹 PASO 1: RECIBIR EL CONTRATO
- Recibirá un correo electrónico con el contrato para firmar.
- Este correo incluye un enlace o un documento adjunto.
- Revise su correo (incluyendo la carpeta de spam).

🔹 PASO 2: REVISAR EL CONTRATO
- Lea TODO el contrato con atención.
- Verifique que sus datos personales estén correctos.
- Revise el objeto del contrato y los entregables.
- Verifique las fechas de inicio y fin.
- Confirme que el valor y la forma de pago sean los acordados.

🔹 PASO 3: FIRMAR DIGITALMENTE
Existen varias formas de firma digital:

OPCIÓN 1: Firma electrónica en la plataforma
- Algunos contratos se firman directamente en el portal de proveedores.
- Debe iniciar sesión y aceptar el contrato.
- Esto genera una firma electrónica con validez legal.

OPCIÓN 2: Firma con certificado digital
- Si tiene un certificado digital (ej: en su cédula digital), puede usarlo.
- Siga las instrucciones del correo para firmar con su certificado.

OPCIÓN 3: Firma manuscrita escaneada
- En algunos casos, puede imprimir, firmar a mano y escanear.
- Luego debe subir el documento firmado al portal.

🔹 PASO 4: CONFIRMAR LA FIRMA
- Después de firmar, recibirá una confirmación.
- El contrato quedará formalizado y vinculante.
- Usted recibirá una copia del contrato firmado.

⚠️ PROBLEMAS COMUNES:
- "No me llega el correo" → Revise spam, verifique su correo.
- "No puedo abrir el enlace" → Use Chrome/Firefox, limpie caché.
- "La firma no se completa" → Verifique su conexión a internet.

💡 CONSEJO:
- Firme dentro del plazo indicado (generalmente 3 a 5 días hábiles).
- Guarde una copia del contrato firmado para sus registros.

¿Necesita ayuda con algún paso específico?"""
    ],

    # ==================== SUPERVISOR ====================
    "supervisor": [
        """👤 SUPERVISIÓN DEL CONTRATO

🔹 ¿QUIÉN ES SU SUPERVISOR?
- Es la persona designada por UNIMINUTO para hacer seguimiento a su contrato.
- Generalmente es su jefe directo o el líder del proyecto.

🔹 FUNCIONES DEL SUPERVISOR
- Aprobar sus entregables.
- Acompañar y guiar su trabajo.
- Resolver dudas sobre el objeto del contrato.
- Verificar el cumplimiento de plazos.
- Notificar cualquier novedad al área de contratación.

🔹 ¿CÓMO CONTACTAR A SU SUPERVISOR?
1. Por correo electrónico (el que aparece en su contrato).
2. Por teléfono o WhatsApp (si le fue proporcionado).
3. A través de reuniones programadas.

🔹 ¿QUÉ DEBE HACER CON SU SUPERVISOR?
- Informar sobre el avance de su trabajo.
- Consultar dudas sobre los entregables.
- Notificar cualquier inconveniente.
- Solicitar retroalimentación sobre sus productos.

🔹 ¿QUÉ PASA SI NO TIENE CONTACTO CON SU SUPERVISOR?
- Comuníquese con el área de contratación de UNIMINUTO.
- Ellos le asignarán un nuevo contacto o resolverán el problema.

💡 CONSEJOS PARA TRABAJAR CON SU SUPERVISOR
- Sea proactivo y comuníquese con frecuencia.
- Cumpla con los plazos acordados.
- Pregunte si tiene dudas (es mejor preguntar que asumir).
- Mantenga un registro de todas las comunicaciones.

⚠️ IMPORTANTE:
- El supervisor es su principal contacto en UNIMINUTO.
- Si tiene problemas con su contrato, hable primero con su supervisor.

¿Necesita más información sobre cómo contactar a su supervisor?"""
    ],

    # ==================== ACTIVIDAD ECONÓMICA ====================
    "actividad_economica": [
        """📋 ACTIVIDAD ECONÓMICA EN EL RUT - GUÍA COMPLETA

🔹 ¿QUÉ ES LA ACTIVIDAD ECONÓMICA?
Es el código (CIIU) que describe la actividad principal que usted realiza para generar ingresos.
La DIAN lo asigna y lo utiliza para determinar sus obligaciones tributarias.

🔹 ¿CUÁL ES LA ACTIVIDAD RECOMENDADA PARA CONTRATAR CON UNIMINUTO?
Se RECOMIENDA el código 8560: "Actividades de apoyo a la educación".
Esta es la actividad que mejor se ajusta a los servicios que presta un contratista de UNIMINUTO Virtual.

🔹 ¿ES OBLIGATORIO TENER 8560?
NO. No es obligatorio. Es una RECOMENDACIÓN.
Puede tener cualquier otra actividad que corresponda a su labor real.
Ejemplos de otras actividades válidas:
- 8530 → Educación (para profesores)
- 7020 → Consultoría
- 7410 → Diseño
- 6201 → Desarrollo de software
- 7110 → Arquitectura e ingeniería

🔹 ¿CÓMO SABER QUÉ ACTIVIDAD DEBO TENER?
- Si da clases o capacita → 8560 o 8530.
- Si asesora o consulta → 7020.
- Si diseña o crea → 7410.
- Si programa o desarrolla → 6201.
- Si tiene otra profesión, use el código que corresponda.

🔹 ¿CÓMO CAMBIAR LA ACTIVIDAD?
1. Ingrese a la DIAN (www.dian.gov.co).
2. Inicie sesión con su usuario.
3. Busque "Actualización RUT".
4. En la sección de actividades, busque y seleccione el código correcto.
5. Guarde los cambios y descargue el RUT actualizado.

⚠️ IMPORTANTE:
- La actividad debe ser REAL. No la invente.
- Si no está seguro, consulte con su contador.
- Recuerde: 8560 es una RECOMENDACIÓN, no una obligación.

¿Qué actividad económica tiene actualmente en su RUT?"""
    ],

    # ==================== RECHAZOS ====================
    "rechazo_sede": [
        """🏢 PROBLEMA CON LA SEDE DE OPERACIONES

La sede correcta es "Rectoría UNIMINUTO Virtual".

❌ Su registro fue rechazado porque seleccionó otra sede.

🔧 CÓMO ARREGLARLO:
1. Solicite el rechazo de su registro actual.
2. Espere la confirmación del rechazo.
3. Vuelva a registrarse seleccionando "Rectoría UNIMINUTO Virtual".
4. Verifique los demás campos.

💡 La mayoría de los rechazos son por este motivo.

¿Ya solicitó el rechazo de su registro?"""
    ],

    "rechazo_regimen": [
        """📋 PROBLEMA CON EL RÉGIMEN

El régimen que debe seleccionar depende de su tipo de persona:

✅ Persona Natural → "Simplificado"
✅ Persona Jurídica / Empresa → "Común"

❌ Si eligió el régimen equivocado, su registro fue rechazado.

🔧 CÓMO ARREGLARLO:
1. Solicite el rechazo de su registro.
2. Vuelva a registrarse con el régimen correcto.
3. Verifique que el tratamiento y la sede también estén bien.

💡 El régimen debe coincidir con lo que dice su RUT.

¿Ya verificó qué tipo de contribuyente es según su RUT?"""
    ],

    "rechazo_tratamiento": [
        """👤 PROBLEMA CON EL TRATAMIENTO

En el campo "Tratamiento" debe seleccionar:

✅ "Señor(a)" → Para la mayoría de los casos.
✅ "Empleado(a)" → Solo si es colaborador de UNIMINUTO.

❌ Si seleccionó el que no corresponde, su registro fue rechazado.

🔧 CÓMO ARREGLARLO:
1. Solicite el rechazo de su registro.
2. Vuelva a registrarse seleccionando el tratamiento correcto.

💡 ¿Es colaborador de UNIMINUTO o externo?
- Si es externo → "Señor(a)".
- Si es empleado → "Empleado(a)".

¿Ya sabe qué opción le corresponde?"""
    ],

    "problemas_registro": [
        """⚠️ PROBLEMAS COMUNES CON EL REGISTRO

Aquí le explico los problemas más frecuentes y cómo solucionarlos:

❌ "Mi registro fue rechazado" → Puede ser por:

1. SEDE INCORRECTA:
   - Debe ser "Rectoría UNIMINUTO Virtual".
   - Solicite el rechazo y vuelva a registrarse en la sede correcta.

2. RÉGIMEN EQUIVOCADO:
   - Natural → Simplificado; Empresa → Común.
   - Corrija y vuelva a intentar.

3. TRATAMIENTO INCORRECTO:
   - Debe ser "Señor(a)" (a menos que sea empleado).
   - Corrija y vuelva a intentar.

4. CORREO NO COINCIDE CON RUT:
   - El correo debe ser el mismo del RUT.
   - Use el correo correcto.

5. DOCUMENTOS CON CONTRASEÑA:
   - Quite la contraseña de los PDF.
   - Vuelva a subirlos.

6. RUT EN TRÁMITE:
   - Espere a que la DIAN lo apruebe.
   - Descargue la versión final.

❌ "No me deja subir documentos"
- Asegúrese de que sean PDF y sin contraseña.
- Pruebe con Chrome o Firefox actualizados.
- Borre la caché del navegador.

Si nada funciona, comuníquese con su supervisor.

¿Cuál es su problema específico?"""
    ],

    # ==================== FUERA DE ALCANCE ====================
    "fuera_de_alcance": [
        """Disculpe, no entendí bien su pregunta.

Puedo ayudarle con estos temas específicos:

📋 Documentos que debe enviar (persona natural o empresa).
🌐 Registro en el portal de proveedores (paso a paso).
🔧 Cómo llenar el formulario de registro (campos clave).
⚠️ Problemas con el registro (rechazos, errores).
📝 Actualización del RUT (marca de agua, actividad económica).
📅 Plazos de documentos (30 días).
🏥 Examen médico ocupacional.
🏦 Certificación bancaria.
📝 Cotización firmada.

Si tiene una pregunta específica, escríbala con sus propias palabras.
¿En qué tema específico necesita ayuda?""",
        """No logré comprender su pregunta.

Le sugiero que me consulte sobre:
- Documentos para contratación (natural o empresa).
- Registro en el portal de proveedores.
- Diligenciamiento del formulario.
- Actualización del RUT.
- Problemas con el registro.

Escriba su consulta de forma más específica y con gusto le ayudo.

¿Sobre qué tema le gustaría que le brinde información?"""
    ]
}


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def extraer_cedula(texto):
    """Extrae un número de cédula de 6 a 12 dígitos del texto"""
    matches = re.findall(r'\b\d{6,12}\b', texto)
    for m in matches:
        if len(m) >= 7:
            return m
        if len(m) >= 6 and not m.startswith('20'):
            return m
    return None


def detectar_intencion(texto):
    """Detecta la intención del mensaje del usuario - ORDEN CORREGIDO"""
    t = texto.lower()
    cedula = extraer_cedula(texto)
    
    # ============================================================
    # 1. RUT (PRIORIDAD MÁXIMA)
    # ============================================================
    if 'rut' in t:
        _crear = ['crear', 'hacer', 'obtener', 'sacar', 'conseguir', 'tramitar', 'solicitar', 
                  'no tengo', 'no he podido', 'nunca', 'primera vez', 'como hago', 'como obtengo',
                  'no sé', 'ayuda', 'quiero', 'necesito', 'tener', 'conseguir']
        if any(p in t for p in _crear):
            return 'crear_rut', cedula
        _actualizar = ['actualizar', 'renovar', 'actualización', 'cambiar', 'modificar', 'vencido', 'vigente']
        if any(p in t for p in _actualizar):
            return 'actualizar_rut', cedula
        _subir = ['subir', 'validar', 'revisar', 'verificar', 'analizar']
        if any(p in t for p in _subir):
            return 'subir_rut', cedula
        return 'que_es_rut', cedula
    
    # ============================================================
    # 2. ARL
    # ============================================================
    if any(p in t for p in ['arl', 'afiliarme', 'riesgos laborales']):
        return 'arl', cedula
    
    # ============================================================
    # 3. DOCUMENTOS
    # ============================================================
    if any(p in t for p in ['documentos', 'papeles', 'requisitos', 'que necesito', 'que me piden']):
        if 'natural' in t or 'independiente' in t:
            return 'documentos_natural', cedula
        if 'empresa' in t or 'juridica' in t or 'jurídica' in t:
            return 'documentos_juridica', cedula
        return 'documentos_requeridos', cedula
    
    # ============================================================
    # 4. ACTIVIDAD ECONÓMICA
    # ============================================================
    if any(p in t for p in ['codigo ciiu', 'actividad economica', '8560', 'que actividad']):
        return 'actividad_economica', cedula
    
    # ============================================================
    # 5. FIRMA DE CONTRATO
    # ============================================================
    if any(p in t for p in ['firmar contrato', 'firma digital', 'firmar digitalmente', 'como firmo']):
        return 'firma_contrato', cedula
    
    # ============================================================
    # 6. SUPERVISOR
    # ============================================================
    if any(p in t for p in ['supervisor', 'supervisora', 'quien es mi supervisor']):
        return 'supervisor', cedula
    
    # ============================================================
    # 7. PORTAL / REGISTRO
    # ============================================================
    if any(p in t for p in ['portal', 'proveedores', 'plataforma']):
        if any(p in t for p in ['problema', 'error', 'no carga', 'no funciona', 'no puedo', 'caído', 'caida', 'falla']):
            return 'problemas_portal', cedula
        if any(p in t for p in ['registro', 'registrarme', 'inscribirme']):
            if any(p in t for p in ['sede', 'regimen', 'tratamiento', 'codigo postal', 'campo']):
                return 'llenar_plataforma', cedula
            return 'portal_proveedores', cedula
        return 'portal_proveedores', cedula
    
    # ============================================================
    # 8. EXAMEN MÉDICO
    # ============================================================
    if any(p in t for p in ['examen medico', 'examen ocupacional', 'examen de ingreso']):
        return 'examen_medico', cedula
    
    # ============================================================
    # 9. PROCESO DE CONTRATACIÓN
    # ============================================================
    _palabras_proceso = ['proceso', 'pasos', 'etapas', 'contratacion', 'contrato', 'procedimiento', 'que debo hacer']
    if any(p in t for p in _palabras_proceso) and not cedula:
        return 'proceso_contratacion', cedula
    
    # ============================================================
    # 10. CÉDULA
    # ============================================================
    if cedula:
        return 'consulta_estado', cedula
    
    # ============================================================
    # 11. SALUDOS (AL FINAL)
    # ============================================================
    if any(p in t for p in ['hola', 'buenos', 'buenas', 'hi', 'hello', 'ayuda', 'saludos', 'buen día']):
        return 'saludo', cedula
    
    # ============================================================
    # 12. RECHAZOS
    # ============================================================
    if any(p in t for p in ['sede', 'rectoría', 'sede operaciones']) and ('rechaz' in t or 'equivoc' in t):
        return 'rechazo_sede', cedula
    if 'regimen' in t and ('rechaz' in t or 'equivoc' in t):
        return 'rechazo_regimen', cedula
    if 'tratamiento' in t and ('rechaz' in t or 'equivoc' in t):
        return 'rechazo_tratamiento', cedula
    
    # ============================================================
    # 13. CLASIFICADOR SEMÁNTICO
    # ============================================================
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
        encabezado = f"\n--- CONTRATO #{numero_contrato} ---\n"
    
    return f"""{encabezado}
📊 Estado: {estado_traducido}

{observacion_traducida}
"""


def detectar_seguimiento(mensaje, usuario):
    """Detecta si el usuario está respondiendo a una pregunta anterior"""
    mensaje_lower = mensaje.lower()
    
    # ===== DETECTAR "si, [campo]" =====
    if 'si' in mensaje_lower or 'sí' in mensaje_lower:
        campos = ['sede', 'regimen', 'tratamiento', 'codigo postal', 'bien', 'servicio', 'correo', 'objeto social', 'persona de contacto']
        for campo in campos:
            if campo in mensaje_lower:
                return campo, mensaje
    
    # ===== DETECTAR "no, hablamos de [tema]" =====
    if any(p in mensaje_lower for p in ['no, hablamos', 'no, estamos hablando', 'no, me refiero']):
        if 'arl' in mensaje_lower:
            return 'arl', mensaje
        if 'rut' in mensaje_lower:
            return 'rut', mensaje
        if 'documentos' in mensaje_lower:
            return 'documentos', mensaje
    
    palabras_seguimiento = ['si', 'sí', 'no', 'ok', 'vale', 'bueno', 'claro', 'necesito', 'ayuda', 'como', 'donde', 'cuando', 'quien', 'que']
    
    if len(mensaje) < 30 and any(p in mensaje_lower for p in palabras_seguimiento):
        ultima_intencion = memoria.obtener_ultima_intencion(usuario)
        ultima_pregunta = memoria.obtener_ultima_pregunta(usuario)
        
        if ultima_intencion:
            if any(p in mensaje_lower for p in ['si', 'sí', 'ok', 'vale', 'bueno', 'claro', 'necesito']):
                return ultima_intencion, ultima_pregunta
            elif 'no' in mensaje_lower:
                return None, None
            if any(p in mensaje_lower for p in ['ninguno', 'nada', 'no tengo', 'no sé']):
                return ultima_intencion, mensaje_lower
    
    # Detectar palabras clave por tema
    if any(p in mensaje_lower for p in ['arl', 'afiliarme', 'riesgos laborales']):
        return 'arl', mensaje
    if any(p in mensaje_lower for p in ['rut', 'actualizar rut']):
        return 'rut', mensaje
    if any(p in mensaje_lower for p in ['documentos', 'papeles', 'certificacion', 'cedula']):
        return 'documentos', mensaje
    
    return None, None


def obtener_respuesta_seguimiento(intencion_anterior, pregunta_anterior):
    """Devuelve una respuesta de seguimiento basada en la intención anterior"""
    
    # Si el usuario dijo "ninguno" o "nada", dar la guía completa
    if pregunta_anterior and any(p in pregunta_anterior for p in ['ninguno', 'nada', 'no tengo', 'no sé']):
        if intencion_anterior in ['crear_rut', 'actualizar_rut', 'subir_rut', 'rut', 'que_es_rut']:
            return random.choice(RESPUESTAS['crear_rut'])
        if intencion_anterior == 'arl':
            return random.choice(RESPUESTAS['arl'])
        if intencion_anterior in ['documentos_natural', 'documentos_requeridos']:
            return random.choice(RESPUESTAS['documentos_natural'])
        if intencion_anterior in ['portal_proveedores', 'llenar_plataforma', 'problemas_portal']:
            return random.choice(RESPUESTAS['portal_proveedores'])
        return random.choice(RESPUESTAS['fuera_de_alcance'])
    
    if intencion_anterior == 'examen_medico':
        return """🏥 CONTINUEMOS CON EL EXAMEN MÉDICO

Para ayudarle mejor con su examen médico, necesito saber:

1. ¿Ya tiene alguna entidad de salud ocupacional en mente?
2. ¿En qué ciudad se encuentra? (puedo recomendarle opciones cercanas)
3. ¿Necesita información sobre el costo o la vigencia?

Dígame cuál de estas opciones le interesa y le amplío la información.

¿O prefiere que le dé una lista de lugares recomendados en su ciudad?"""
    
    elif intencion_anterior == 'arl':
        return """🏥 CONTINUEMOS CON LA ARL

Para ayudarle mejor con su afiliación a ARL, necesito saber:

1. ¿Ya tiene alguna ARL en mente?
2. ¿En qué ciudad se encuentra? (puedo recomendarle opciones cercanas)
3. ¿Necesita ayuda con el proceso de afiliación?

Dígame su situación y le doy una guía personalizada.

¿O prefiere que le dé los pasos específicos para afiliarse?"""
    
    elif intencion_anterior in ['documentos_natural', 'documentos_requeridos']:
        return """📋 CONTINUEMOS CON LOS DOCUMENTOS

Para ayudarle mejor con sus documentos, necesito saber:

1. ¿Es persona natural o empresa?
2. ¿Ya tiene alguno de los documentos listos?
3. ¿Cuál documento le genera más dificultad?

Dígame su situación y le doy una guía más específica.

¿Qué documento necesita ayuda para obtener?"""
    
    elif intencion_anterior in ['portal_proveedores', 'llenar_plataforma', 'problemas_portal']:
        return """🌐 CONTINUEMOS CON EL REGISTRO EN EL PORTAL

Para ayudarle mejor con el registro, necesito saber:

1. ¿Ya inició el registro en el portal?
2. ¿En qué campo específico tiene dudas?
3. ¿Ya le rechazaron el registro?

Dígame en qué punto está y le doy ayuda personalizada.

¿En qué paso del registro se encuentra?"""
    
    elif intencion_anterior in ['actualizar_rut', 'rut', 'crear_rut', 'subir_rut', 'que_es_rut']:
        if intencion_anterior == 'crear_rut' or intencion_anterior == 'que_es_rut':
            return random.choice(RESPUESTAS['crear_rut'])
        return """📝 CONTINUEMOS CON EL RUT

Para ayudarle mejor con su RUT, necesito saber:

1. ¿Ya tiene usuario en la DIAN?
2. ¿Cuál es el problema específico que tiene?
3. ¿Ya intentó actualizarlo o crearlo?

Dígame su situación y le doy una guía paso a paso.

¿Qué problema específico tiene con su RUT?"""
    
    else:
        return """Entiendo que necesita ayuda con el tema que estábamos conversando.

¿Podría indicarme qué información adicional necesita sobre este tema?

Puedo ayudarle con:
- RUT (creación o actualización).
- Documentos para contratación.
- Registro en el portal.
- Examen médico.
- ARL y afiliación.
- Cualquier otra duda del proceso.

¿Sobre qué aspecto específico necesita más información?"""


def detectar_campo_formulario(texto):
    """Detecta qué campo del formulario está preguntando el usuario"""
    t = texto.lower()
    
    # NO capturar "supervisor" aquí
    if any(p in t for p in ['supervisor', 'supervisora', 'quien es mi supervisor']):
        return None
    
    if any(p in t for p in ['sede', 'sede operaciones', 'rectoría']):
        return 'sede'
    if any(p in t for p in ['bien o servicio', 'bien o serv', 'bien', 'servicio']):
        return 'bien_servicio'
    if any(p in t for p in ['tratamiento', 'señor', 'empleado']):
        return 'tratamiento'
    if any(p in t for p in ['regimen', 'régimen', 'simplificado', 'comun']):
        return 'regimen'
    if any(p in t for p in ['correo', 'email', 'correo electronico']):
        return 'correo'
    if any(p in t for p in ['codigo postal', 'código postal', 'codigo', 'postal']):
        return 'codigo_postal'
    if any(p in t for p in ['objeto social', 'objeto']):
        return 'objeto_social'
    if any(p in t for p in ['persona de contacto', 'contacto', 'persona contacto']):
        return 'persona_contacto'
    
    return None


# ============================================================
# FUNCIÓN PRINCIPAL: responder_contratista
# ============================================================

def responder_contratista(mensaje, usuario="anonimo"):
    """
    Responde al contratista con la información más relevante
    """
    mensaje_lower = mensaje.lower()
    
    # 1. GUARDAR EL MENSAJE DEL USUARIO EN MEMORIA
    memoria.guardar_mensaje(usuario, mensaje, tipo="usuario")
    
    # 2. VERIFICAR SI ES UN SEGUIMIENTO DE CONVERSACIÓN
    intencion_seguimiento, pregunta_anterior = detectar_seguimiento(mensaje, usuario)
    
    if intencion_seguimiento:
        # Si el seguimiento es un campo del formulario, responder directamente
        campo_map = {
            'sede': 'sede',
            'regimen': 'regimen',
            'tratamiento': 'tratamiento',
            'codigo postal': 'codigo_postal',
            'bien': 'bien_servicio',
            'servicio': 'bien_servicio',
            'correo': 'correo',
            'objeto social': 'objeto_social',
            'persona de contacto': 'persona_contacto'
        }
        if intencion_seguimiento in campo_map:
            campo_clave = campo_map[intencion_seguimiento]
            if campo_clave in RESPUESTAS_CAMPOS:
                respuesta = RESPUESTAS_CAMPOS[campo_clave]
                memoria.guardar_mensaje(usuario, respuesta, tipo="bot", intencion=f"campo_{campo_clave}")
                memoria.guardar_intencion(usuario, campo_clave)
                return respuesta
        
        # Si el usuario dijo "si" o "necesito"
        if any(p in mensaje_lower for p in ['si', 'sí', 'ok', 'vale', 'bueno', 'claro', 'necesito']):
            respuesta = obtener_respuesta_seguimiento(intencion_seguimiento, pregunta_anterior)
            memoria.guardar_mensaje(usuario, respuesta, tipo="bot", intencion=intencion_seguimiento)
            return respuesta
        elif 'no' in mensaje_lower:
            memoria.limpiar(usuario)
    
    # 3. DETECTAR CAMPO DEL FORMULARIO
    campo = detectar_campo_formulario(mensaje)
    if campo and campo in RESPUESTAS_CAMPOS:
        respuesta = RESPUESTAS_CAMPOS[campo]
        memoria.guardar_mensaje(usuario, respuesta, tipo="bot", intencion=f"campo_{campo}")
        memoria.guardar_intencion(usuario, campo)
        return respuesta
    
    # 4. DETECTAR INTENCIÓN
    intencion, cedula = detectar_intencion(mensaje)
    
    if cedula:
        memoria.guardar_cedula(usuario, cedula)
    
    memoria.guardar_intencion(usuario, intencion)
    
    # 5. SISTEMA DE CONOCIMIENTO
    if any(p in mensaje_lower for p in PATRONES_RUT):
        respuesta = respuesta_rut(mensaje)
        memoria.guardar_mensaje(usuario, respuesta, tipo="bot", intencion="rut")
        return respuesta
    
    if any(p in mensaje_lower for p in PATRONES_DOCUMENTOS):
        respuesta = respuesta_documentos(mensaje)
        memoria.guardar_mensaje(usuario, respuesta, tipo="bot", intencion="documentos")
        return respuesta
    
    if any(p in mensaje_lower for p in PATRONES_PORTAL):
        respuesta = respuesta_portal(mensaje)
        memoria.guardar_mensaje(usuario, respuesta, tipo="bot", intencion="portal")
        return respuesta
    
    if any(p in mensaje_lower for p in PATRONES_CONTRATOS):
        respuesta = respuesta_contratos(mensaje)
        memoria.guardar_mensaje(usuario, respuesta, tipo="bot", intencion="contratos")
        return respuesta
    
    # 6. INTENCIONES ESPECÍFICAS
    if intencion in RESPUESTAS:
        respuesta = random.choice(RESPUESTAS[intencion])
        memoria.guardar_mensaje(usuario, respuesta, tipo="bot", intencion=intencion)
        return respuesta
    
    # 7. CONSULTAR ESTADO (CON CÉDULA)
    if cedula:
        registros = lector.buscar_por_cedula(cedula)
        
        if registros:
            info_principal = lector.obtener_info_contratista(registros[0])
            
            respuesta = f"""📋 ESTADO DE SU PROCESO

👤 Nombre: {info_principal['nombre']}
🆔 Cédula: {info_principal['cedula']}
📅 Año: {info_principal['año']}

═══════════════════════════════════════
"""
            respuesta += formatear_contrato(info_principal)
            
            if len(registros) > 1:
                respuesta += f"\n═══════════════════════════════════════\n"
                respuesta += f"📋 TIENE {len(registros)} CONTRATOS REGISTRADOS\n"
                respuesta += "═══════════════════════════════════════\n"
                for i, otro in enumerate(registros[1:], 2):
                    info_otro = lector.obtener_info_contratista(otro)
                    respuesta += formatear_contrato(info_otro, i)
            
            respuesta += "\n═══════════════════════════════════════\n"
            respuesta += "¿En qué más le ayudo?"
            memoria.guardar_mensaje(usuario, respuesta, tipo="bot", intencion="estado")
            return respuesta
        else:
            return f"""❌ No encontré información con la cédula {cedula}.

Verifique que el número esté bien escrito. Si acaba de firmar contrato, puede que su información aún no esté cargada en el sistema (tarda 24-48 horas).

¿En qué más le puedo ayudar?"""
    
    # 8. RESPUESTA POR DEFECTO
    respuesta = random.choice(RESPUESTAS['fuera_de_alcance'])
    memoria.guardar_mensaje(usuario, respuesta, tipo="bot", intencion="fuera_de_alcance")
    return respuesta