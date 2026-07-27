# chatbot/conocimiento/rut.py
"""
Base de conocimiento sobre RUT - COMPLETO
Todas las preguntas y respuestas sobre RUT
"""
import re

# ============================================================
# PATRONES PARA DETECTAR PREGUNTAS DE RUT
# ============================================================

PATRONES_RUT = [
    # Generales
    "que es el rut", "que significa rut", "para que sirve el rut", "quien me da el rut",
    "donde saco el rut", "como obtengo el rut", "el rut es obligatorio", "que es rut",
    "rut significa", "rut para que", "rut obligatorio", "rut quien lo da",
    
    # Actualización
    "como actualizo el rut", "como renovar el rut", "cada cuanto actualizar el rut",
    "rut vencido", "rut viejo", "toca actualizar rut", "donde actualizo el rut",
    "actualizar rut en la dian", "pasos para actualizar rut", "renovar rut",
    "rut actualizado", "rut nuevo", "rut en la dian", "como renovar el rut",
    "cada cuanto debo actualizar el rut", "rut vencido que hago", "mi rut esta viejo",
    
    # Marcas de agua
    "que significa copia en el rut", "que significa certificado en el rut",
    "que significa en tramite en el rut", "rut en tramite sirve", "rut copia sirve",
    "rut certificado sirve", "cual marca de agua debe tener el rut", "rut sin marca de agua",
    "copia rut", "certificado rut", "en tramite rut", "marca de agua rut",
    "rut en tramite", "rut con copia", "rut con certificado",
    
    # Actividad económica
    "que actividad economica debe tener el rut", "que es el codigo 8560",
    "8560 que significa", "actividad economica para educacion", "que codigo ciiu debo tener",
    "como cambio mi actividad economica", "no tengo actividad 8560", "actividad economica rut",
    "codigo 8560", "actividad 8560", "cambiar actividad rut", "que actividad poner en el rut",
    "8560 actividades de apoyo a la educacion", "codigo ciiu 8560", "actividad economica recomendada",
    
    # Vigencia
    "cuanto tiempo dura el rut", "rut de 30 dias", "rut con mas de 30 dias",
    "rut viejo no sirve", "porque el rut debe ser reciente", "vigencia del rut",
    "rut 30 dias", "rut vencido", "rut con fecha vencida", "plazo del rut",
    
    # Problemas
    "rut rechazado", "porque rechazan mi rut", "rut no valido", "rut incorrecto",
    "error en el rut", "rut no coincide con cedula", "problemas con el rut",
    "rut rechazado", "rut invalido", "rut no sirve", "rut no coincide",
    
    # DIAN
    "como entrar a la dian", "usuario dian", "contraseña dian", "no puedo entrar a la dian",
    "la dian no funciona", "dian caida", "registrarse en la dian", "dian",
    "pagina de la dian", "dian no carga", "dian caida", "usuario y contraseña dian",
    
    # Extranjeros
    "rut para extranjeros", "extranjero sin rut", "cedula de extranjeria y rut",
    "permiso de trabajo y rut", "rut extranjero", "extranjero rut", "rut para extranjeros",
]

# ============================================================
# RESPUESTAS SOBRE RUT - COMPLETAS
# ============================================================

def respuesta_rut(pregunta):
    """
    Devuelve la respuesta más adecuada para una pregunta sobre RUT
    """
    p = pregunta.lower()
    
    # ============================================================
    # 1. QUÉ ES EL RUT
    # ============================================================
    if any(x in p for x in ['que es el rut', 'que significa rut', 'para que sirve el rut', 'que es rut']):
        return """📋 ¿QUÉ ES EL RUT?

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

    # ============================================================
    # 2. CÓMO ACTUALIZAR EL RUT
    # ============================================================
    if any(x in p for x in ['como actualizo el rut', 'como renovar el rut', 'actualizar rut', 'renovar rut', 'rut actualizado', 'pasos para actualizar rut']):
        return """📝 CÓMO ACTUALIZAR SU RUT - PASO A PASO

Actualizar su RUT es un proceso completamente en línea que puede hacer desde su casa u oficina. Siga estos pasos:

🔹 PASO 1: INGRESE A LA DIAN
- Abra su navegador (Chrome o Firefox recomendados).
- Vaya a la página oficial: www.dian.gov.co

🔹 PASO 2: INICIE SESIÓN
- Haga clic en "Iniciar sesión" o "Usuario DIAN".
- Ingrese su usuario y contraseña.
- Si aún no tiene usuario, debe crearlo seleccionando "Registrarse" o "Crear usuario".
- Si olvidó su contraseña, use la opción "Recuperar contraseña".

🔹 PASO 3: BUSQUE "ACTUALIZACIÓN RUT"
- En el menú principal, busque "Actualización RUT" o "Actualización de datos".
- Esta opción generalmente está en "Servicios en línea" o "Trámites".

🔹 PASO 4: REVISE Y ACTUALICE SUS DATOS
Verifique que todos sus datos estén correctos:
- Dirección de residencia: debe ser su dirección actual.
- Correo electrónico: debe ser un correo que revise con frecuencia.
- Número de teléfono: debe estar activo.
- Actividad económica: debe corresponder a su labor real.

🔹 PASO 5: ACTUALICE LA ACTIVIDAD ECONÓMICA (Si es necesario)
- Si trabaja en educación, use el código 8560 (Actividades de apoyo a la educación).
- Si tiene otra actividad, use el código que corresponda a su labor real.
- NO invente una actividad. Debe ser real.

🔹 PASO 6: DESCARGUE EL RUT ACTUALIZADO
- Después de confirmar los cambios, busque la opción "Descargar RUT".
- Seleccione la opción con marca de agua "Copia" o "Certificado".
- NUNCA descargue la versión "En trámite" para contratar con UNIMINUTO.

🔹 PASO 7: VERIFIQUE EL DOCUMENTO
Revise que su nuevo RUT tenga:
- ✅ Fecha de expedición menor a 30 días.
- ✅ Marca de agua: "Copia" o "Certificado".
- ✅ Su nombre completo y cédula correctos.
- ✅ Actividad económica correcta.
- ✅ Dirección y correo actualizados.

⚠️ IMPORTANTE:
- Si su RUT dice "En trámite", NO es válido. Debe esperar a que la DIAN lo apruebe.
- La actualización es gratuita y no necesita ir a ninguna oficina.
- Si tiene problemas, la DIAN tiene líneas de atención telefónica.

¿Tiene problemas en algún paso en particular?"""

    # ============================================================
    # 3. MARCAS DE AGUA
    # ============================================================
    if any(x in p for x in ['marca de agua', 'copia en el rut', 'certificado en el rut', 'en tramite en el rut', 'que significa copia', 'que significa certificado']):
        return """📋 MARCAS DE AGUA DEL RUT - QUÉ SIGNIFICA CADA UNA

Su RUT puede tener diferentes marcas de agua. Solo dos son válidas para contratar con UNIMINUTO:

✅ "COPIA"
- Significa que el documento es una copia fiel del original registrado en la DIAN.
- Es completamente válido y aceptado por UNIMINUTO.
- Esta es la marca de agua más común y recomendada.

✅ "CERTIFICADO"
- Significa que la DIAN certifica oficialmente que los datos son correctos.
- Es completamente válido y aceptado por UNIMINUTO.
- Tiene el mismo valor que "Copia".

✅ "ACTUALIZACIÓN"
- Significa que el documento fue actualizado recientemente.
- Es válido si tiene menos de 30 días de expedición.
- Si tiene más de 30 días, debe renovarlo.

❌ "EN TRÁMITE"
- Significa que su solicitud de actualización está en proceso.
- NO es válido para contratar con UNIMINUTO.
- Debe esperar a que la DIAN apruebe y descargar la versión final.
- Tiempo estimado: 24 a 72 horas hábiles.

❌ "BORRADOR"
- Significa que el documento no ha sido formalizado.
- NO es válido para contratar.
- Debe completar el proceso en la DIAN.

❌ SIN MARCA DE AGUA
- Significa que no es un documento oficial.
- NO es válido para contratar.
- Debe descargarlo correctamente desde la DIAN.

💡 RECOMENDACIÓN:
Siempre descargue su RUT con la marca de agua "Copia" o "Certificado".
Si su RUT dice "En trámite", espere un par de días y vuelva a intentarlo.

¿Qué marca de agua tiene su RUT actual?"""

    # ============================================================
    # 4. ACTIVIDAD ECONÓMICA
    # ============================================================
    if any(x in p for x in ['actividad economica', '8560', 'codigo ciiu', 'que actividad', 'cambiar actividad']):
        return """📋 ACTIVIDAD ECONÓMICA EN EL RUT - GUÍA COMPLETA

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
- Una actividad incorrecta puede generar problemas tributarios futuros.
- Recuerde: 8560 es una RECOMENDACIÓN, no una obligación.

¿Qué actividad económica tiene actualmente en su RUT?"""

    # ============================================================
    # 5. VIGENCIA (30 DÍAS)
    # ============================================================
    if any(x in p for x in ['30 dias', 'vigencia', 'vencido', 'viejo', 'antiguo', 'plazo', 'cuanto dura']):
        return """📅 VIGENCIA DEL RUT - PLAZO DE 30 DÍAS

🔹 ¿POR QUÉ DEBE SER RECIENTE?
UNIMINUTO exige que el RUT tenga menos de 30 días de expedición para garantizar que su información esté actualizada y sea confiable.

🔹 ¿QUÉ PASA SI TIENE MÁS DE 30 DÍAS?
- Su RUT NO será válido para el proceso de contratación.
- Su proceso se retrasará hasta que lo actualice.
- Deberá ingresar a la DIAN, actualizar sus datos y descargar un RUT nuevo.

🔹 ¿CÓMO VERIFICAR LA FECHA DE EXPEDICIÓN?
- En la primera página del RUT, busque la fecha de expedición.
- Si es un documento digital, aparece en el encabezado o en el pie de página.
- Si no encuentra la fecha, puede que no sea un documento válido.

🔹 ¿QUÉ HACER SI SU RUT ESTÁ VENCIDO?
1. Ingrese a la DIAN (www.dian.gov.co).
2. Inicie sesión con su usuario.
3. Busque "Actualización RUT".
4. Revise que todos sus datos estén correctos.
5. Descargue el RUT nuevamente con fecha actualizada.
6. Verifique que tenga menos de 30 días.

🔹 ¿PUEDO USAR UN RUT CON 31 DÍAS?
No. Aunque sea solo un día más, no será válido.
UNIMINUTO es estricto con el plazo de 30 días.

💡 CONSEJO:
Mantenga su RUT siempre actualizado. Revíselo antes de cada proceso de contratación.
Si sabe que va a contratar, actualícelo con anticipación para evitar retrasos.

¿Cuándo fue la última vez que actualizó su RUT?"""

    # ============================================================
    # 6. PROBLEMAS CON EL RUT
    # ============================================================
    if any(x in p for x in ['rechazado', 'rechazo', 'no valido', 'incorrecto', 'error', 'problema', 'no sirve']):
        return """⚠️ PROBLEMAS CON EL RUT - SOLUCIONES COMPLETAS

🔹 PROBLEMA 1: "EN TRÁMITE"
- Causa: La DIAN aún no ha aprobado su actualización.
- Solución: Espere 24 a 72 horas hábiles.
- Si pasa más tiempo, comuníquese con la DIAN.

🔹 PROBLEMA 2: ACTIVIDAD ECONÓMICA INCORRECTA
- Causa: La actividad no corresponde a su labor.
- Solución: Actualice la actividad en la DIAN.
- Recuerde: 8560 es recomendada, no obligatoria.

🔹 PROBLEMA 3: FECHA VENCIDA (MÁS DE 30 DÍAS)
- Causa: El RUT tiene más de 30 días de expedición.
- Solución: Actualice el RUT en la DIAN.

🔹 PROBLEMA 4: CÉDULA INCORRECTA
- Causa: La cédula en el RUT no coincide con la suya.
- Solución: Revise sus datos en la DIAN y corríjalos.

🔹 PROBLEMA 5: NOMBRE INCORRECTO
- Causa: El nombre no coincide con el de su cédula.
- Solución: Corrija el nombre en la DIAN.

🔹 PROBLEMA 6: SIN MARCA DE AGUA
- Causa: El RUT no tiene "copia" o "certificado".
- Solución: Descargue el RUT nuevamente con la marca correcta.

🔹 PROBLEMA 7: DOCUMENTO ILEGIBLE
- Causa: El PDF está escaneado con mala calidad.
- Solución: Descargue el RUT directamente de la DIAN (no lo escanee).

📌 SI NADA FUNCIONA:
- Comuníquese con la DIAN: línea de atención 01-8000-912-123.
- Consulte con su contador.
- Pregunte a su supervisor en UNIMINUTO.

¿Cuál de estos problemas está presentando?"""

    # ============================================================
    # 7. DIAN (PORTAL)
    # ============================================================
    if any(x in p for x in ['dian', 'entrar a la dian', 'usuario dian', 'contraseña dian', 'dian no funciona', 'dian caida']):
        return """🌐 PORTAL DE LA DIAN - CÓMO USARLO

🔹 ¿CÓMO INGRESAR A LA DIAN?
1. Abra su navegador (Chrome o Firefox).
2. Vaya a: www.dian.gov.co
3. Haga clic en "Iniciar sesión" (esquina superior derecha).
4. Ingrese su usuario y contraseña.

🔹 ¿CÓMO CREAR UN USUARIO EN LA DIAN?
1. Vaya a www.dian.gov.co.
2. Busque la opción "Registrarse" o "Crear usuario".
3. Complete todos los campos requeridos.
4. Confirme su correo electrónico.
5. Espere la activación de su cuenta.

🔹 ¿QUÉ HACER SI OLVIDÓ SU CONTRASEÑA?
1. Vaya a la página de inicio de sesión.
2. Haga clic en "¿Olvidó su contraseña?".
3. Ingrese su usuario y correo.
4. Siga las instrucciones para recuperarla.

🔹 ¿LA DIAN NO CARGA O NO FUNCIONA?
- Espere unos minutos y vuelva a intentar.
- Pruebe con otro navegador (Chrome, Firefox, Edge).
- Limpie la caché del navegador.
- Intente en horarios de menor tráfico (temprano en la mañana).

🔹 ¿NÚMEROS DE CONTACTO DE LA DIAN?
- Línea nacional: 01-8000-912-123.
- Línea Bogotá: (601) 307-8077.
- Horario de atención: 8:00 a.m. a 4:00 p.m.

⚠️ IMPORTANTE:
- La DIAN es la única entidad que puede emitir y actualizar RUT.
- No confíe en sitios web externos que ofrezcan hacerlo por usted.
- Todo el proceso debe hacerse directamente en el portal oficial.

¿Tiene problemas específicos con la página de la DIAN?"""

    # ============================================================
    # 8. EXTRANJEROS
    # ============================================================
    if any(x in p for x in ['extranjero', 'extranjera', 'cedula de extranjeria', 'permiso', 'ppt']):
        return """🌎 RUT PARA EXTRANJEROS - GUÍA COMPLETA

🔹 ¿PUEDE UN EXTRANJERO TENER RUT?
Sí. Todos los extranjeros con residencia o permiso de trabajo en Colombia pueden obtener RUT.

🔹 ¿QUÉ DOCUMENTOS NECESITA?
- Cédula de Extranjería (vigente).
- Pasaporte vigente.
- Permiso de Trabajo (si aplica).
- Permiso de Protección Temporal (PPT) si tiene.

🔹 ¿CÓMO OBTENER EL RUT SI ES EXTRANJERO?
1. Ingrese a la DIAN: www.dian.gov.co
2. Regístrese como usuario con su Cédula de Extranjería.
3. Siga el mismo proceso que un ciudadano colombiano.
4. La DIAN asignará un NIT para extranjeros.

🔹 ¿QUÉ CÓDIGO DE ACTIVIDAD USAR?
- Si trabaja en educación: 8560 (recomendado).
- Si trabaja en otra área: use el código que corresponda a su labor.

🔹 ¿QUÉ PASA SI NO TIENE RUT?
No puede contratar con UNIMINUTO.
Debe obtenerlo antes de iniciar cualquier proceso.

🔹 CASOS ESPECIALES:
- Permiso de Protección Temporal (PPT): válido para obtener RUT.
- Visa de trabajo: también permite obtener RUT.
- Residencia definitiva: puede obtener RUT sin restricciones.

🔹 ¿QUÉ PASA SI SU CÉDULA DE EXTRANJERÍA ESTÁ VENCIDA?
No podrá tramitar ni actualizar su RUT.
Renueve su documento antes de iniciar el proceso.

⚠️ IMPORTANTE:
- El RUT para extranjeros funciona igual que para colombianos.
- Debe mantenerlo actualizado (menos de 30 días).
- La actividad económica debe ser real.

¿Tiene Cédula de Extranjería o Permiso de Trabajo?"""

    # ============================================================
    # 9. RESPUESTA POR DEFECTO SOBRE RUT
    # ============================================================
    return """📋 INFORMACIÓN GENERAL SOBRE EL RUT

El RUT (Registro Único Tributario) es su documento de identidad ante la DIAN y es obligatorio para contratar con UNIMINUTO Virtual.

🔹 REQUISITOS BÁSICOS:
- ✅ Fecha de expedición: menor a 30 días.
- ✅ Marca de agua: "Copia" o "Certificado".
- ✅ NO "En trámite" ni "Borrador".
- ✅ Actividad económica: puede ser 8560 (recomendada) u otra.
- ✅ Cédula y nombre: deben coincidir con los suyos.

🔹 ¿DÓNDE LO OBTIENE?
- www.dian.gov.co
- Debe crear un usuario y solicitar el RUT.

🔹 ¿CÓMO LO ACTUALIZA?
1. Ingrese a la DIAN con su usuario.
2. Busque "Actualización RUT".
3. Revise y actualice sus datos.
4. Descargue el RUT con marca "Copia" o "Certificado".

🔹 ¿QUÉ HACER SI TIENE PROBLEMAS?
- Consulte su caso específico en la DIAN (01-8000-912-123).
- Pregunte a su supervisor en UNIMINUTO.
- Pregúnteme sobre su situación específica.

¿Sobre qué aspecto del RUT necesita más información?"""