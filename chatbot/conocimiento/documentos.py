# chatbot/conocimiento/documentos.py
"""
Base de conocimiento sobre DOCUMENTOS
Todas las preguntas y respuestas sobre documentos de contratación
"""

# ============================================================
# PATRONES PARA DETECTAR PREGUNTAS DE DOCUMENTOS
# ============================================================

PATRONES_DOCUMENTOS = [
    # Generales
    "que documentos necesito", "que papeles debo enviar", "requisitos para contratar",
    "documentos para contratar", "que me piden", "cuales son los requisitos",
    "que papeles van", "documentos requeridos", "lista de documentos",
    
    # Persona natural
    "documentos persona natural", "papeles persona natural", "que necesita un natural",
    "independiente que documentos", "natural requisitos", "persona natural que papeles",
    
    # Persona jurídica
    "documentos persona juridica", "papeles empresa", "que necesita una empresa",
    "empresa documentos", "juridica requisitos", "persona juridica que papeles",
    
    # Cédula
    "cedula", "cedula de ciudadania", "cedula ambas caras", "cedula escaneada",
    "cedula foto", "cedula pdf", "cedula vigencia",
    
    # Certificación bancaria
    "certificacion bancaria", "certificado bancario", "cuenta bancaria",
    "certificacion banco", "certificacion de cuenta", "banco certificado",
    
    # RUT
    "rut documento", "rut actualizado", "rut vigencia", "rut marca de agua",
    "rut actividad", "rut copia", "rut certificado",
    
    # ARL
    "arl", "certificacion arl", "arl activa", "arl independiente", "arl empresa",
    
    # Examen médico
    "examen medico", "examen ocupacional", "examen de ingreso", "examen laboral",
    "examen medico donde", "examen medico vigencia",
    
    # Formato Excel
    "ingreso independientes", "formato excel", "excel diligenciado",
    "formato ingreso", "formato independientes",
    
    # Cámara de Comercio
    "camara de comercio", "camara y comercio", "certificado camara",
    "existencia y representacion", "camara vigencia",
]

# ============================================================
# RESPUESTAS SOBRE DOCUMENTOS
# ============================================================

def respuesta_documentos(pregunta):
    """
    Devuelve la respuesta más adecuada para una pregunta sobre documentos
    """
    p = pregunta.lower()
    
    # ============================================================
    # 1. DOCUMENTOS EN GENERAL
    # ============================================================
    if any(x in p for x in ['que documentos necesito', 'que papeles debo enviar', 'requisitos', 'que me piden', 'que papeles van']):
        return """📋 DOCUMENTOS REQUERIDOS PARA CONTRATAR CON UNIMINUTO

Los documentos que debe presentar dependen de su tipo de contratación:

📌 PERSONA NATURAL (INDEPENDIENTE):
1. 📄 Cédula de ciudadanía (ambas caras, PDF).
2. 🏦 Certificación bancaria (máx. 30 días, PDF).
3. 📋 RUT actualizado (máx. 30 días, "copia" o "certificado").
4. 📊 Formato Excel "Ingreso Independientes" (diligenciado).
5. 🏥 Certificación de ARL (activa como independiente).
6. 🏥 Examen médico ocupacional (máx. 3 años).

📌 PERSONA JURÍDICA (EMPRESA):
1. 📄 Cédula del representante legal (ambas caras).
2. 🏦 Certificación bancaria de la empresa (máx. 30 días).
3. 📋 RUT de la empresa actualizado (máx. 30 días).
4. 📑 Cámara de Comercio (máx. 30 días).
5. 📄 Cédula del representante legal (nuevamente).
6. 🏥 Certificación de la ARL de la empresa.
7. 🏥 Examen médico ocupacional del representante legal (máx. 3 años).

📌 REQUISITOS GENERALES PARA AMBOS:
- ✅ Todos en formato PDF.
- ✅ Sin contraseña.
- ✅ Fecha de expedición NO mayor a 30 días (excepto examen médico).
- ✅ Documentos legibles y completos.

⚠️ IMPORTANTE:
- Si falta algún documento, su proceso se retrasa.
- Los documentos se suben en el portal de proveedores.
- Su supervisor será notificado si hay retrasos.

¿Es persona natural o empresa? Dígame y le doy la lista exacta con más detalles."""

    # ============================================================
    # 2. DOCUMENTOS PERSONA NATURAL
    # ============================================================
    if any(x in p for x in ['persona natural', 'independiente', 'natural', 'cedula', 'soy natural']):
        return """📋 DOCUMENTOS PARA PERSONA NATURAL (CONTRATISTA INDEPENDIENTE)

A continuación, la lista detallada de documentos que debe presentar:

📄 1. CÉDULA DE CIUDADANÍA (AMBAS CARAS)
- Escanee ambas caras y unifíquelas en un solo PDF.
- Asegúrese de que se vean claramente todos los datos.
- Formato: PDF, sin contraseña.
- NO debe ser foto desde el celular (a menos que sea muy clara).

🏦 2. CERTIFICACIÓN BANCARIA
- Fecha de expedición NO mayor a 30 días.
- Debe estar a su nombre (igual al RUT).
- Solicítela en su banco (app, web o sucursal).
- Formato: PDF, sin contraseña.

📋 3. RUT ACTUALIZADO
- Fecha de expedición NO mayor a 30 días.
- Marca de agua: "copia" o "certificado" (NO "en trámite").
- Actividad económica: 8560 es recomendada, pero puede tener otra.
- Formato: PDF, sin contraseña.

📊 4. FORMATO EXCEL "INGRESO INDEPENDIENTES"
- Diligéncielo completamente con su información personal.
- Guarde el archivo con su nombre y cédula.
- Formato: Excel (.xlsx o .xls).
- Lo recibió por correo cuando inició el proceso.

🏥 5. CERTIFICACIÓN DE ARL
- Activa como trabajador independiente.
- Certificación reciente (no mayor a 30 días).
- Formato: PDF, sin contraseña.

🏥 6. EXAMEN MÉDICO OCUPACIONAL
- Vigencia máxima de 3 años.
- Debe indicar que es APTO para el cargo.
- Formato: PDF, sin contraseña.

⚠️ TODOS los documentos deben estar en PDF y sin contraseña.

¿Cuál de estos documentos necesita ayuda para obtener?"""

    # ============================================================
    # 3. DOCUMENTOS EMPRESA
    # ============================================================
    if any(x in p for x in ['persona juridica', 'juridica', 'empresa', 'camara de comercio', 'representante legal']):
        return """📋 DOCUMENTOS PARA PERSONA JURÍDICA (EMPRESA)

A continuación, la lista detallada de documentos que debe presentar su empresa:

📄 1. CÉDULA DEL REPRESENTANTE LEGAL (AMBAS CARAS)
- Escanee ambas caras en un solo PDF.
- Asegúrese de que se vean claramente todos los datos.
- Formato: PDF, sin contraseña.

🏦 2. CERTIFICACIÓN BANCARIA DE LA EMPRESA
- Fecha de expedición NO mayor a 30 días.
- A nombre de la empresa (igual al RUT).
- Solicítela en el banco (app, web o sucursal).
- Formato: PDF, sin contraseña.

📋 3. RUT DE LA EMPRESA ACTUALIZADO
- Fecha de expedición NO mayor a 30 días.
- Marca de agua: "copia" o "certificado".
- Actividad económica: 8560 es recomendada, pero puede tener otra.
- Formato: PDF, sin contraseña.

📑 4. CÁMARA DE COMERCIO
- Fecha de expedición NO mayor a 30 días.
- Debe incluir el certificado de existencia y representación legal.
- Solicítela en la Cámara de Comercio de su ciudad.
- Formato: PDF, sin contraseña.

📄 5. CÉDULA DEL REPRESENTANTE LEGAL (nuevamente)
- Algunas secciones del portal la solicitan otra vez.
- Use el mismo documento que en el punto 1.

🏥 6. CERTIFICACIÓN DE LA ARL DE LA EMPRESA
- Activa y al día con sus obligaciones.
- Certificación reciente (no mayor a 30 días).
- Formato: PDF, sin contraseña.

🏥 7. EXAMEN MÉDICO OCUPACIONAL DEL REPRESENTANTE LEGAL
- Vigencia máxima de 3 años.
- Debe indicar que es APTO para el cargo.
- Formato: PDF, sin contraseña.

⚠️ TODOS los documentos en PDF y sin contraseña.

¿Necesita ayuda con algún documento en específico?"""

    # ============================================================
    # 4. CÉDULA
    # ============================================================
    if 'cedula' in p and 'rut' not in p:
        return """📄 INFORMACIÓN SOBRE LA CÉDULA DE CIUDADANÍA

🔹 ¿QUÉ DEBO ENTREGAR?
- Ambas caras de la cédula de ciudadanía.
- Deben estar escaneadas en un solo archivo PDF.
- Si tiene cédula de extranjería, también sirve.

🔹 ¿CÓMO DEBE SER EL ARCHIVO?
- Formato: PDF (NO JPG, NO Word).
- Sin contraseña.
- Legible: que se vean claramente todos los datos.

🔹 ¿PUEDO TOMARLE FOTO CON EL CELULAR?
- Sí, siempre que la foto sea clara y se vean todos los datos.
- Preferiblemente escaneada con una aplicación de escaneo (no solo la foto).

🔹 ¿QUÉ PASA SI MI CÉDULA ESTÁ DETERIORADA?
- Si no se leen bien los datos, puede ser rechazada.
- Si está muy deteriorada, solicite una copia auténtica en la Registraduría.

🔹 ¿CÉDULA DE EXTRANJERÍA?
- Sí, también es válida.
- Debe tener su Permiso de Trabajo vigente (si aplica).
- El proceso es el mismo que con la cédula colombiana.

⚠️ IMPORTANTE:
- La cédula debe estar vigente (no vencida).
- El nombre en la cédula debe coincidir con el RUT.

¿Tiene cédula colombiana o de extranjería?"""

    # ============================================================
    # 5. CERTIFICACIÓN BANCARIA
    # ============================================================
    if 'certificacion bancaria' in p or 'certificado bancario' in p:
        return """🏦 CERTIFICACIÓN BANCARIA - GUÍA COMPLETA

🔹 ¿QUÉ ES?
Es un documento oficial que expide su banco donde certifica que usted (o su empresa) tiene una cuenta activa a su nombre.

🔹 ¿PARA QUÉ SIRVE?
Sirve para que UNIMINUTO pueda realizar los pagos de su contrato de manera segura a la cuenta que usted indique.

🔹 REQUISITOS:
- ✅ Fecha de expedición: NO mayor a 30 días.
- ✅ Formato: PDF.
- ✅ Sin contraseña.
- ✅ El nombre debe coincidir EXACTAMENTE con su RUT y cédula.

🔹 ¿DÓNDE LA OBTENGO?
1. En su banco:
   - Por la aplicación móvil (muchos bancos la generan automáticamente).
   - Por la página web del banco (banca en línea).
   - En una oficina física (solicite el certificado de cuenta).

2. Bancos que sirven:
   - Davivienda
   - Bancolombia
   - BBVA
   - Banco de Bogotá
   - Caja Social
   - Nequi (si tiene cuenta de ahorros)
   - Daviplata
   - Lulo Bank
   - Nu Bank

🔹 ¿QUÉ DATOS DEBE TENER?
- ✅ Su nombre completo (igual al RUT).
- ✅ Número de cuenta (ahorros o corriente).
- ✅ Tipo de cuenta.
- ✅ Fecha de expedición.

🔹 ¿CUENTA DE NÓMINA O AHORROS?
Ambas sirven, siempre que estén a su nombre.

💡 CONSEJO:
Puede pedir la certificación bancaria por la banca en línea, es más rápido y no tiene que ir a una oficina.

¿Tiene cuenta de ahorros o corriente?"""

    # ============================================================
    # 6. EXAMEN MÉDICO
    # ============================================================
    if 'examen medico' in p or 'examen ocupacional' in p:
        return """🏥 EXAMEN MÉDICO OCUPACIONAL - GUÍA COMPLETA

🔹 ¿QUÉ ES?
Es un examen de salud que evalúa si usted está en condiciones físicas y mentales adecuadas para desempeñar el cargo o servicio para el cual fue contratado.

🔹 ¿ES OBLIGATORIO?
Sí. Es un requisito indispensable para todos los contratistas de UNIMINUTO Virtual.

🔹 VIGENCIA:
Debe tener una vigencia máxima de 3 años.
Si tiene más de 3 años, debe renovarlo.

🔹 ¿DÓNDE LO PUEDO HACER?
Puede realizarlo en cualquier entidad de salud ocupacional autorizada:
- ARL (Administradora de Riesgos Laborales).
- Clínicas ocupacionales.
- IPS (Instituciones Prestadoras de Salud) que ofrezcan el servicio.

🔹 ¿CÓMO LO SOLICITO?
1. Busque una entidad de salud ocupacional cerca de usted.
2. Pida una cita para examen médico ocupacional.
3. Asista a la cita con su documento de identidad.
4. El médico le realizará los exámenes correspondientes.
5. Solicite que le entreguen el certificado en formato PDF.

🔹 ¿QUÉ DEBO ENTREGAR?
- El certificado o resultado del examen.
- Debe indicar que usted es APTO para el cargo.
- El documento debe estar en formato PDF y sin contraseña.

🔹 COSTO:
- El costo varía según la entidad y los exámenes requeridos.
- Generalmente está entre $50,000 y $150,000.
- Consulte con su ARL, a veces cubren el examen.

⚠️ IMPORTANTE:
- Si su examen tiene más de 3 años, debe renovarlo.
- El examen es obligatorio, no puede omitirlo.
- Si no lo presenta, su proceso de contratación se retrasará.

💡 CONSEJO:
Si no sabe dónde hacerlo, consulte con su ARL o con el área de talento humano de UNIMINUTO Virtual.

¿Necesita ayuda para encontrar dónde hacer su examen médico?"""

    # ============================================================
    # 7. ARL
    # ============================================================
    if 'arl' in p or 'riesgos laborales' in p:
        return """🏥 CERTIFICACIÓN DE ARL - GUÍA COMPLETA

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

¿Ya tiene ARL o necesita ayuda para afiliarse?"""

    # ============================================================
    # 8. FORMATO EXCEL
    # ============================================================
    if 'excel' in p or 'ingreso independientes' in p or 'formato' in p:
        return """📊 FORMATO EXCEL "INGRESO INDEPENDIENTES"

🔹 ¿QUÉ ES?
Es un formato en Excel que debe diligenciar con su información personal y profesional.

🔹 ¿DÓNDE LO OBTENGO?
- Le fue enviado por correo electrónico cuando inició el proceso.
- También puede pedírmelo en el chat y se lo proporciono.

🔹 ¿CÓMO LO DILIGENCIO?
1. Abra el archivo en Excel.
2. Complete todos los campos requeridos:
   - Su nombre completo.
   - Número de cédula.
   - Dirección de residencia.
   - Teléfono de contacto.
   - Correo electrónico.
   - Información profesional (si aplica).
3. Guarde el archivo con su nombre y cédula.
   - Ejemplo: "JuanPerez_12345678.xlsx"

🔹 ¿QUÉ FORMATO DEBO ENTREGAR?
- Excel (.xlsx o .xls).
- El archivo debe estar completo y legible.

⚠️ IMPORTANTE:
- No deje campos obligatorios en blanco.
- Asegúrese de que la información sea correcta.
- Si tiene dudas, pregúnteme y le ayudo.

¿Ya tiene el formato o necesita que se lo envíe?"""

    # ============================================================
    # 9. RESPUESTA POR DEFECTO
    # ============================================================
    return """📋 INFORMACIÓN GENERAL SOBRE DOCUMENTOS

Los documentos que debe presentar dependen de su tipo de contratación:

📌 PERSONA NATURAL:
- Cédula (ambas caras).
- Certificación bancaria (30 días).
- RUT actualizado (30 días).
- Formato Excel "Ingreso Independientes".
- ARL activa.
- Examen médico (3 años).

📌 EMPRESA:
- Cédula del representante (ambas caras).
- Certificación bancaria de la empresa (30 días).
- RUT de la empresa (30 días).
- Cámara de Comercio (30 días).
- ARL de la empresa.
- Examen médico del representante (3 años).

✅ TODOS en PDF y sin contraseña.

¿Es persona natural o empresa? Dígame y le doy la lista exacta con más detalles."""