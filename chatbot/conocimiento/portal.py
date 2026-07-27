# chatbot/conocimiento/portal.py
"""
Base de conocimiento sobre PORTAL DE PROVEEDORES
Todas las preguntas y respuestas sobre el portal
"""

# ============================================================
# PATRONES PARA DETECTAR PREGUNTAS DE PORTAL
# ============================================================

PATRONES_PORTAL = [
    # Generales
    "portal de proveedores", "registro en el portal", "como me registro", "donde me registro",
    "portal proveedores", "plataforma proveedores", "registro proveedores", "inscribirme como proveedor",
    
    # Problemas
    "no abre el portal", "portal no carga", "error en el portal", "portal caido",
    "no puedo entrar al portal", "portal no funciona", "pagina no carga",
    
    # Usuario y contraseña
    "usuario portal", "contraseña portal", "recuperar contraseña portal",
    "olvide mi usuario", "olvide mi contraseña", "no recuerdo contraseña",
    
    # Campos
    "sede operaciones", "bien o servicio", "tratamiento", "regimen", "codigo postal",
    "que pongo en sede", "que pongo en regimen", "que pongo en tratamiento",
]

# ============================================================
# RESPUESTAS SOBRE PORTAL
# ============================================================

def respuesta_portal(pregunta):
    """
    Devuelve la respuesta más adecuada para una pregunta sobre el portal
    """
    p = pregunta.lower()
    
    # ============================================================
    # 1. REGISTRO EN EL PORTAL
    # ============================================================
    if any(x in p for x in ['como me registro', 'registro en el portal', 'portal proveedores', 'inscribirme']):
        return """🌐 REGISTRO EN EL PORTAL DE PROVEEDORES - GUÍA COMPLETA

🔹 PASO 1: ACCEDER AL PORTAL
- Ingrese al siguiente enlace: 👉 https://proveedores.uniminuto.edu
- Use Chrome o Firefox para mejor compatibilidad.

🔹 PASO 2: INICIAR EL REGISTRO
- Haga clic en el botón "Registrarse" (esquina superior derecha).

🔹 PASO 3: DILIGENCIAR EL FORMULARIO
Complete todos los campos con atención:

🏢 SEDE DE OPERACIONES:
Debe seleccionar "Rectoría UNIMINUTO Virtual".
Es la primera opción de la lista.
Si selecciona cualquier otra sede, su registro será rechazado.

📦 BIEN O SERVICIO:
Seleccione "Servicio".
Luego elija la categoría que corresponda a su labor.

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

🔹 PASO 4: ENVIAR EL REGISTRO
- Revise que todos los datos estén correctos.
- Haga clic en "Enviar" o "Registrar".

🔹 PASO 5: ESPERAR LA VALIDACIÓN
- El sistema validará su información.
- Recibirá un correo de confirmación si todo está correcto.
- Si hay errores, el sistema le notificará para que los corrija.

💡 CONSEJOS IMPORTANTES:
- La mayoría de los rechazos son por Sede, Régimen o Tratamiento.
- Después de registrarse, debe enviar los documentos requeridos.
- Si tiene dudas, pregúnteme sobre algún campo específico.

¿Necesita ayuda con algún campo en particular?"""

    # ============================================================
    # 2. PROBLEMAS CON EL PORTAL
    # ============================================================
    if any(x in p for x in ['no abre', 'no carga', 'error', 'caido', 'no funciona', 'no puedo entrar']):
        return """⚠️ PROBLEMAS CON EL PORTAL - SOLUCIONES

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

    # ============================================================
    # 3. CAMPOS DEL FORMULARIO
    # ============================================================
    if any(x in p for x in ['sede', 'regimen', 'tratamiento', 'codigo postal', 'bien o servicio']):
        return """🔧 CÓMO LLENAR LOS CAMPOS DEL FORMULARIO

🏢 SEDE DE OPERACIONES
- Debe seleccionar: "Rectoría UNIMINUTO Virtual".
- Es la primera opción de la lista.
- Si selecciona otra, su registro será rechazado.

📦 BIEN O SERVICIO
- Seleccione: "Servicio".
- Luego elija la categoría correspondiente a su labor.
- Ejemplos: Educación, Consultoría, Tecnología, etc.

👤 TRATAMIENTO
- "Señor(a)" → Para personas naturales/independientes.
- "Empleado(a)" → Solo si es colaborador de UNIMINUTO.
- Si no es colaborador, siempre use "Señor(a)".

📋 RÉGIMEN
- "Simplificado" → Persona Natural (independiente).
- "Común" → Persona Jurídica (empresa).
- Si selecciona el régimen equivocado, su registro será rechazado.

📧 CORREO ELECTRÓNICO
- Debe ser el mismo que aparece en su RUT.
- Allí recibirá toda la comunicación oficial.
- Verifíquelo antes de enviar.

📮 CÓDIGO POSTAL
- Busque el código postal de su ciudad en Google.
- Ejemplo: "código postal Bogotá".
- No lo invente, el sistema lo valida.

📄 OBJETO SOCIAL
- Describa brevemente la actividad económica que realiza.
- Ejemplo: "Servicios de consultoría educativa".
- No escriba información personal, solo la actividad profesional.

💡 LA MAYORÍA DE RECHAZOS SON POR:
1. Sede incorrecta.
2. Régimen equivocado.
3. Tratamiento mal seleccionado.

¿Tiene duda con algún campo en específico?"""

    # ============================================================
    # 4. USUARIO Y CONTRASEÑA
    # ============================================================
    if any(x in p for x in ['usuario', 'contraseña', 'recuperar', 'olvide', 'no recuerdo']):
        return """🔐 USUARIO Y CONTRASEÑA DEL PORTAL

🔹 ¿CÓMO CREAR MI USUARIO?
1. Vaya a https://proveedores.uniminuto.edu.
2. Haga clic en "Registrarse".
3. Complete todos los campos.
4. Al final, se creará su usuario automáticamente.

🔹 ¿OLVIDÓ SU CONTRASEÑA?
1. Vaya a la página de inicio de sesión.
2. Haga clic en "¿Olvidó su contraseña?".
3. Ingrese su usuario y correo electrónico.
4. Siga las instrucciones que recibirá por correo.
5. Cree una nueva contraseña.

🔹 ¿OLVIDÓ SU USUARIO?
1. Contacte al área de contratación de UNIMINUTO.
2. Ellos pueden ayudarle a recuperar su usuario.
3. También puede usar su correo electrónico como usuario.

🔹 ¿QUÉ HACER SI NO RECIBO EL CORREO PARA RESTABLECER?
1. Revise la carpeta de spam o correo no deseado.
2. Verifique que el correo registrado sea correcto.
3. Espere al menos 10 minutos.
4. Si no llega, intente nuevamente.

⚠️ RECOMENDACIONES DE SEGURIDAD:
- Use una contraseña segura (mayúsculas, números, símbolos).
- No comparta su contraseña con nadie.
- Si sospecha que alguien la conoce, cámbiela inmediatamente.

¿Necesita ayuda para restablecer su contraseña?"""

    # ============================================================
    # 5. RESPUESTA POR DEFECTO
    # ============================================================
    return """🌐 PORTAL DE PROVEEDORES - INFORMACIÓN GENERAL

El portal de proveedores es la plataforma donde debe registrarse y subir sus documentos para contratar con UNIMINUTO Virtual.

🔹 ACCESO:
https://proveedores.uniminuto.edu

🔹 CAMPOS CLAVE:
- Sede: "Rectoría UNIMINUTO Virtual".
- Bien o Servicio: "Servicio".
- Tratamiento: "Señor(a)" o "Empleado(a)".
- Régimen: "Simplificado" o "Común".
- Correo: igual al de su RUT.

🔹 PROBLEMAS COMUNES:
- No carga la página → pruebe con otro navegador.
- Error al registrarse → revise los campos clave.
- No recibe correo → revise spam.

🔹 ¿NECESITA AYUDA CON ALGÚN CAMPO ESPECÍFICO?
Pregúnteme y le ayudo.

¿En qué parte del portal necesita ayuda?"""