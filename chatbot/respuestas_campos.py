



# backend/chatbot/respuestas_campos.py
"""
Respuestas específicas para cada campo del formulario de registro en el portal de proveedores
Generado por IA y validado para el contexto de UNIMINUTO Virtual
"""

RESPUESTAS_CAMPOS = {
    "sede": """📌 SEDE DE OPERACIONES

🔹 ¿QUÉ ES?
La sede de operaciones corresponde a la dependencia de UNIMINUTO para la cual usted prestará el bien o servicio. Este campo permite que el contrato y toda la documentación sean asociados correctamente a la unidad solicitante.

🔹 ¿CÓMO DILIGENCIARLO?
1. Ubique el campo "Sede de Operaciones".
2. Haga clic sobre la lista desplegable.
3. Busque la opción "Rectoría UNIMINUTO Virtual".
4. Selecciónela haciendo clic sobre ella.
5. Antes de continuar, confirme que el nombre seleccionado sea exactamente "Rectoría UNIMINUTO Virtual".

⚠️ ERRORES COMUNES:
• Seleccionar otra sede como Bogotá, Rectoría General, Cundinamarca o cualquier otra.
• Elegir una sede porque "parece similar".
• Dejar el campo sin seleccionar.
• Cambiar la sede después de iniciar el registro.

Estos errores pueden ocasionar devoluciones del registro o retrasos en el proceso de contratación.

💡 CONSEJOS PRÁCTICOS:
• Siempre revise el nombre completo antes de guardar.
• No seleccione la sede basándose únicamente en la ciudad donde vive.
• La sede debe corresponder a la dependencia contratante y no necesariamente a su ubicación.

📌 EJEMPLO:
✅ Correcto:
Rectoría UNIMINUTO Virtual

❌ Incorrecto:
- Bogotá
- Rectoría General
- Cundinamarca
- Bello
- Antioquia

Recuerde que para los procesos de contratación de la Rectoría Virtual, la opción correcta es únicamente "Rectoría UNIMINUTO Virtual".

❓¿Necesita ayuda con otro campo del formulario?""",

    "bien_servicio": """📌 BIEN O SERVICIO

🔹 ¿QUÉ ES?
Este campo identifica el tipo de contratación que realizará con UNIMINUTO. Debe indicar si suministrará un bien (producto físico) o prestará un servicio (actividad profesional, técnica o de apoyo).

🔹 ¿CÓMO DILIGENCIARLO?
1. Ubique el campo "Bien o Servicio".
2. Revise las opciones disponibles.
3. Si realizará actividades profesionales, asesorías, apoyo administrativo, desarrollo de software, consultoría, capacitaciones o similares, seleccione "Servicio".
4. Si venderá productos físicos como equipos, muebles, papelería o materiales, seleccione "Bien".
5. Confirme la selección antes de continuar.

⚠️ ERRORES COMUNES:
• Elegir "Bien" cuando realmente prestará un servicio.
• Escoger una opción al azar para avanzar más rápido.
• No verificar qué tipo de contrato realizará.

Seleccionar la opción incorrecta puede generar inconsistencias durante la validación del proveedor.

💡 CONSEJOS PRÁCTICOS:
• Pregúntese qué entregará a UNIMINUTO.
• Si entrega un producto físico, normalmente corresponde a un bien.
• Si realiza una actividad profesional o técnica, normalmente corresponde a un servicio.

📌 EJEMPLOS:
✅ Servicio:
- Honorarios profesionales.
- Desarrollo de software.
- Consultoría.
- Capacitación.

✅ Bien:
- Venta de computadores.
- Venta de escritorios.
- Venta de impresoras.

Si tiene dudas sobre cuál seleccionar, confirme primero el objeto de su contrato.

❓¿Su contrato corresponde a un bien o a un servicio?""",

    "tratamiento": """📌 TRATAMIENTO

🔹 ¿QUÉ ES?
El tratamiento es la forma de dirigirse al proveedor dentro del sistema. No afecta el contrato ni las condiciones de pago; únicamente determina cómo aparecerá identificado en comunicaciones y documentos.

Generalmente encontrará opciones como "Señor(a)" y "Empleado(a)".

🔹 ¿CÓMO DILIGENCIARLO?
1. Abra la lista del campo "Tratamiento".
2. Revise las opciones disponibles.
3. Si se registra como proveedor independiente o persona natural, seleccione "Señor(a)".
4. Si recibió una instrucción específica para utilizar otra opción, siga la indicación entregada por UNIMINUTO.
5. Guarde la selección.

⚠️ ERRORES COMUNES:
• Pensar que este campo cambia el tipo de contrato.
• Seleccionar "Empleado(a)" porque actualmente trabaja en otra empresa.
• Elegir una opción diferente sin indicación.

Este campo únicamente corresponde al tratamiento o forma de dirigirse a usted.

💡 CONSEJOS PRÁCTICOS:
• Si nadie le indicó lo contrario, normalmente la opción utilizada para proveedores es "Señor(a)".
• No confunda este campo con el tipo de vinculación laboral.

📌 EJEMPLO:
Nombre:
María Rodríguez

Tratamiento:
✅ Señor(a)

No importa si es ingeniera, contador o abogado; el tratamiento únicamente corresponde a la forma de dirigirse al proveedor.

❓¿Desea que le explique cuándo utilizar "Empleado(a)" y cuándo "Señor(a)"?""",

    "regimen": """📌 RÉGIMEN

🔹 ¿QUÉ ES?
Este campo corresponde al régimen tributario al que pertenece el proveedor según su información registrada ante la DIAN. Es un dato fiscal importante para la facturación y el proceso de contratación.

🔹 ¿CÓMO DILIGENCIARLO?
1. Consulte su RUT actualizado.
2. Verifique el régimen al que pertenece.
3. Seleccione exactamente el mismo régimen que aparece en su información tributaria.
4. No elija una opción basándose en suposiciones.

⚠️ ERRORES COMUNES:
• Elegir un régimen diferente al registrado ante la DIAN.
• Contestar sin revisar el RUT.
• Confundir responsabilidades tributarias con el régimen.

Ingresar un régimen incorrecto puede generar observaciones durante la validación documental.

💡 CONSEJOS PRÁCTICOS:
• Antes de diligenciar este campo, tenga su RUT a la mano.
• Si tiene dudas sobre su régimen tributario, consulte primero su información tributaria antes de continuar.
• Nunca seleccione una opción solo porque "suena correcta".

📌 EJEMPLO:
Si en su documentación tributaria corresponde al régimen simplificado, deberá seleccionar esa misma opción.
Si corresponde al régimen común, deberá seleccionar régimen común.

Lo importante es que exista total coincidencia entre el formulario y la información oficial.

❓¿Desea ayuda para identificar el régimen que aparece en su RUT?""",

    "correo": """📌 CORREO ELECTRÓNICO

🔹 ¿QUÉ ES?
El correo electrónico será el principal medio de comunicación entre usted y UNIMINUTO. A esta dirección podrán enviarse notificaciones, solicitudes de documentos, observaciones, novedades del proceso y otra información relacionada con la contratación.

🔹 ¿CÓMO DILIGENCIARLO?
1. Escriba un correo electrónico activo.
2. Verifique que esté correctamente escrito.
3. Revise que no tenga espacios antes o después.
4. Confirme que pueda acceder normalmente a esa cuenta.

⚠️ ERRORES COMUNES:
• Escribir mal el dominio (gmai.com, hotmal.com).
• Omitir el símbolo @.
• Utilizar un correo que ya no revisa.
• Incluir espacios en blanco.

Estos errores pueden impedir que reciba comunicaciones importantes.

💡 CONSEJOS PRÁCTICOS:
• Utilice un correo de uso frecuente.
• Revise periódicamente la bandeja de entrada y la carpeta de spam.
• Si es posible, utilice siempre el mismo correo durante todo el proceso contractual.

📌 EJEMPLO:
✅ proveedor@gmail.com
✅ juan.perez@empresa.com.co

❌ proveedorgmail.com
❌ proveedor@gmai.con
❌ proveedor @gmail.com

Antes de continuar, vuelva a leer el correo completo para asegurarse de que esté correctamente escrito.

❓¿Necesita ayuda para verificar si su correo quedó correctamente diligenciado?""",

    "codigo_postal": """📌 CÓDIGO POSTAL

🔹 ¿QUÉ ES?
El código postal es un número asignado por el servicio postal colombiano que identifica la zona geográfica donde se encuentra su dirección. Este dato facilita la ubicación del proveedor y hace parte de la información de contacto.

🔹 ¿CÓMO DILIGENCIARLO?
1. Identifique la dirección donde reside o donde se encuentra registrada su empresa.
2. Consulte el código postal correspondiente a esa dirección.
3. Escriba únicamente el código postal, sin letras ni símbolos.
4. Verifique que el número corresponda exactamente a su ubicación.

⚠️ ERRORES COMUNES:
• Escribir el número de la dirección en lugar del código postal.
• Colocar el código postal de otra ciudad.
• Inventar un número para continuar el registro.
• Dejar el campo vacío.

💡 CONSEJOS PRÁCTICOS:
• Si no conoce su código postal, consúltelo antes de finalizar el formulario.
• Revise cuidadosamente que corresponda a la dirección registrada.
• No copie el código postal de otra persona.

📌 EJEMPLO:
Si su dirección corresponde a una zona cuyo código postal es 110111, deberá escribir únicamente:

110111

No agregue palabras como "Bogotá", "Colombia" ni caracteres adicionales.

Recuerde que este dato debe coincidir con la ubicación registrada en su información de contacto.

❓¿Conoce su código postal o necesita ayuda para identificarlo?""",

    "objeto_social": """📌 OBJETO SOCIAL

🔹 ¿QUÉ ES?
El objeto social describe las actividades económicas que usted o su empresa están autorizados para desarrollar. Esta información permite verificar que las actividades contratadas sean compatibles con su registro legal.

🔹 ¿CÓMO DILIGENCIARLO?
1. Consulte su Certificado de Cámara de Comercio o el documento correspondiente.
2. Ubique el apartado denominado "Objeto Social".
3. Copie la información respetando su contenido.
4. Revise que no queden palabras incompletas.

⚠️ ERRORES COMUNES:
• Escribir únicamente una palabra.
• Resumir demasiado el objeto social.
• Inventar actividades diferentes.
• Escribir funciones que no aparecen en sus documentos.

Estas inconsistencias pueden generar observaciones durante la revisión documental.

💡 CONSEJOS PRÁCTICOS:
• Copie la información directamente desde el documento oficial.
• Evite modificar la redacción.
• Si su objeto social es extenso, mantenga la información más relevante relacionada con la actividad contractual, siempre respetando el documento.

📌 EJEMPLO:
"La sociedad tiene por objeto la prestación de servicios de consultoría, desarrollo de software, soporte tecnológico, mantenimiento de sistemas de información y actividades relacionadas."

Mientras más coincida con sus documentos oficiales, más sencillo será el proceso de validación.

❓¿Desea ayuda para identificar cuál es su objeto social?""",

    "persona_contacto": """📌 PERSONA DE CONTACTO

🔹 ¿QUÉ ES?
La persona de contacto es quien atenderá las comunicaciones relacionadas con el proceso de contratación. Puede ser el mismo proveedor o una persona autorizada para responder requerimientos, solicitudes y novedades.

🔹 ¿CÓMO DILIGENCIARLO?
1. Escriba el nombre completo de la persona.
2. Verifique que sea quien realmente atenderá las comunicaciones.
3. Confirme que los datos de contacto asociados sean correctos.
4. Continúe con el siguiente campo.

⚠️ ERRORES COMUNES:
• Escribir únicamente el primer nombre.
• Registrar una persona que desconoce el proceso.
• Utilizar apodos o nombres incompletos.
• Colocar datos de una persona que ya no trabaja en la empresa.

Esto puede ocasionar retrasos cuando sea necesario realizar validaciones o solicitar documentos adicionales.

💡 CONSEJOS PRÁCTICOS:
• Si usted mismo gestionará el proceso, puede registrar su propio nombre.
• Mantenga actualizado este dato si cambia el responsable.
• Verifique que la persona pueda responder oportunamente.

📌 EJEMPLO:
Nombre:
Juan Carlos Pérez Gómez

No escriba:
❌ Juan
❌ JP
❌ Contabilidad

Siempre utilice nombres completos para facilitar la identificación durante el proceso contractual.

❓¿La persona de contacto será usted mismo o otra persona autorizada?"""
}