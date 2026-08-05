# chatbot/flujos.py
"""
Definición de todos los flujos conversacionales
Cada flujo es una lista de pasos
VERSIÓN CORREGIDA - Opción "Volver al inicio" y eliminación de precios
"""

FLUJOS = {
    # ============================================================
    # FLUJO: REGISTRO EN EL PORTAL
    # ============================================================
    "registro": {
        "nombre": "Registro en el portal de proveedores",
        "descripcion": "Guía paso a paso para registrarse en el portal",
        "pasos": [
            {
                "id": "paso_1",
                "titulo": "PASO 1: Acceder al portal",
                "contenido": "🔹 Ingrese al siguiente enlace: 👉 https://proveedores.uniminuto.edu\n🔹 Use Chrome o Firefox para mejor compatibilidad.",
                "detalle": "El portal de proveedores es la plataforma donde se registra para contratar con UNIMINUTO. Si no puede acceder, verifique su conexión a internet o pruebe con otro navegador.",
                "pregunta": "¿Ya pudo acceder al portal sin problemas?",
                "opciones": ["Si", "No, tengo problemas"],
                "respuesta_no": {
                    "mensaje": "❌ Si no puede acceder al portal, pruebe estas soluciones:\n\n1. Verifique su conexión a internet.\n2. Pruebe con otro navegador (Chrome, Firefox, Edge).\n3. Limpie la caché del navegador (Ctrl + Shift + Supr en Chrome).\n4. Intente en modo incógnito (Ctrl + Shift + N).\n5. Si sigue sin funcionar, espere unos minutos y vuelva a intentar.\n\nSi el problema persiste, comuníquese con el área de contratación de UNIMINUTO Virtual."
                }
            },
            {
                "id": "paso_2",
                "titulo": "PASO 2: Iniciar el registro",
                "contenido": "🔹 Haga clic en el botón 'Registrarse'\n🔹 Está en la esquina superior derecha de la pantalla.",
                "detalle": "El botón 'Registrarse' es de color azul y dice 'Registrarse' o 'Sign Up'. Si no lo ve, intente limpiar la caché del navegador o use el modo incógnito.",
                "pregunta": "¿Ya encontró y presionó el botón 'Registrarse'?",
                "opciones": ["Si", "No, no lo veo"],
                "respuesta_no": {
                    "mensaje": "🔍 Si no ve el botón 'Registrarse', pruebe estas opciones:\n\n1. Asegúrese de estar en la página correcta: https://proveedores.uniminuto.edu\n2. El botón está en la esquina superior derecha, al lado del botón de inicio de sesión.\n3. Si no lo ve, limpie la caché del navegador (Ctrl + Shift + Supr en Chrome).\n4. Pruebe con otro navegador (Firefox, Edge).\n5. Si sigue sin verlo, es posible que ya esté registrado. Intente iniciar sesión con su correo y contraseña.\n\nSi no recuerda su contraseña, use la opción '¿Olvidó su contraseña?'"
                }
            },
            {
                "id": "paso_3",
                "titulo": "PASO 3: Diligenciar el formulario - Datos generales",
                "contenido": "🔹 Complete los campos del formulario con atención:\n\n🏢 SEDE DE OPERACIONES: 'Rectoría UNIMINUTO Virtual' (primera opción)\n📦 BIEN O SERVICIO: 'Servicio' + categoría correspondiente\n👤 TRATAMIENTO: 'Señor(a)' (o 'Empleado(a)' si es colaborador)",
                "detalle": "Los errores más comunes son: seleccionar otra sede, elegir el régimen equivocado o poner un tratamiento incorrecto. Si tiene duda en algún campo, pregúnteme y le explico en detalle.",
                "pregunta": "¿Tiene duda con algún campo de estos?",
                "opciones": ["No, continuar", "Si, tengo una duda"],
                "respuesta_no": {
                    "mensaje": "📌 No se preocupe, aquí le explico cada campo en detalle:\n\n🏢 SEDE DE OPERACIONES:\n- Debe seleccionar 'Rectoría UNIMINUTO Virtual'.\n- Es la PRIMERA opción de la lista.\n- Si selecciona cualquier otra sede, su registro será rechazado.\n\n📦 BIEN O SERVICIO:\n- Seleccione 'Servicio'.\n- Luego elija la categoría que corresponda a su labor.\n- Si no sabe qué categoría elegir, pregúnteme y le ayudo.\n\n👤 TRATAMIENTO:\n- 'Señor(a)' → si es persona natural/independiente.\n- 'Empleado(a)' → solo si es colaborador de UNIMINUTO.\n- Si no es colaborador, siempre use 'Señor(a)'.\n\n💡 La mayoría de los rechazos son por Sede o Tratamiento incorrectos."
                }
            },
            {
                "id": "paso_4",
                "titulo": "PASO 4: Diligenciar el formulario - Campos clave",
                "contenido": "🔹 Complete los siguientes campos:\n\n📋 RÉGIMEN: 'Simplificado' (natural) o 'Común' (empresa)\n📧 CORREO: El mismo que aparece en su RUT\n📮 CÓDIGO POSTAL: Busque el de su ciudad en Google",
                "detalle": "El régimen debe coincidir con su RUT. Si es persona natural, use 'Simplificado'. Si es empresa, use 'Común'. El código postal es de 6 dígitos, búsquelo en Google: 'código postal [nombre de su ciudad]'.",
                "pregunta": "¿Tiene duda con algún campo de estos?",
                "opciones": ["No, continuar", "Si, tengo una duda"],
                "respuesta_no": {
                    "mensaje": "📌 Aquí le explico cada campo con más detalle:\n\n📋 RÉGIMEN:\n- Si es persona natural (independiente): seleccione 'Simplificado'.\n- Si es persona jurídica (empresa): seleccione 'Común'.\n- Si selecciona el régimen equivocado, su registro será rechazado.\n- Consulte su RUT para confirmar su régimen.\n\n📧 CORREO ELECTRÓNICO:\n- Debe ser el mismo que aparece en su RUT.\n- Allí recibirá toda la comunicación oficial.\n- Verifíquelo antes de enviar.\n\n📮 CÓDIGO POSTAL:\n- Busque el código postal de su ciudad en Google.\n- Ejemplo: 'código postal Bogotá'.\n- No lo invente, el sistema lo valida.\n- Es de 6 dígitos (ej: 110111).\n\n💡 La mayoría de los rechazos son por Régimen o Código Postal incorrectos."
                }
            },
            {
                "id": "paso_5",
                "titulo": "PASO 5: Enviar el registro",
                "contenido": "🔹 Revise toda la información\n🔹 Haga clic en 'Enviar' o 'Registrar'\n🔹 Espere la confirmación del sistema",
                "detalle": "Antes de enviar, verifique: que la sede sea la correcta, que el correo sea el del RUT, y que el régimen coincida. Si todo está bien, presione 'Enviar'.",
                "pregunta": "¿Ya envió el formulario o quiere que le ayude a revisar antes de enviar?",
                "opciones": ["Ya lo envié", "Quiero revisar antes"],
                "respuesta_no": {
                    "mensaje": "✅ Revisemos juntos antes de enviar:\n\n🔍 LISTA DE VERIFICACIÓN:\n1. Sede: ¿seleccionó 'Rectoría UNIMINUTO Virtual'?\n2. Bien o Servicio: ¿seleccionó 'Servicio' y la categoría correcta?\n3. Tratamiento: ¿es 'Señor(a)'?\n4. Régimen: ¿corresponde a su RUT (Simplificado o Común)?\n5. Correo: ¿es el mismo de su RUT?\n6. Código Postal: ¿es el de su ciudad?\n\nSi todo está correcto, puede enviar el formulario con confianza.\nSi tiene dudas, pregúnteme antes de enviar."
                }
            },
            {
                "id": "paso_6",
                "titulo": "PASO 6: Después del registro — ¿Qué sigue?",
                "contenido": "🔹 ¡Formulario enviado! Ahora debe completar estos pasos:\n\n📌 PASO 1: SUBIR DOCUMENTOS AL PORTAL\n- Vaya al portal de proveedores: https://proveedores.uniminuto.edu\n- Inicie sesión con su usuario y contraseña.\n- Busque la sección 'Documentos' o 'Subir documentos'.\n- Suba TODOS los documentos requeridos en PDF y sin contraseña.\n\n📌 PASO 2: RADICAR DOCUMENTOS POR CORREO\n- Envíe los mismos documentos al correo de su supervisor.\n- Si no tiene el correo de su supervisor, contacte al área de contratación.\n- Asegúrese de que los documentos estén en PDF y sin contraseña.\n\n📌 PASO 3: ESPERAR LA VALIDACIÓN\n- El área de contratación revisará sus documentos.\n- Esto puede tardar de 1 a 3 días hábiles.\n- Recibirá un correo de confirmación si todo está correcto.\n- Si hay errores, le notificarán para que los corrija.\n\n📌 PASO 4: FIRMAR EL CONTRATO\n- Una vez aprobado, recibirá el contrato para firmar digitalmente.\n- Siga las instrucciones del correo para firmarlo.\n- Guarde una copia del contrato firmado.",
                "detalle": "📌 IMPORTANTE:\n\n1. Si no sube los documentos al portal, el proceso no avanzará.\n2. Si no envía los documentos por correo a su supervisor, el proceso se retrasará.\n3. Todos los documentos deben estar en PDF y sin contraseña.\n4. La validación puede tardar de 1 a 3 días hábiles. Sea paciente.\n5. Si su registro es rechazado, no se desanime. Corrija los errores y vuelva a intentarlo.\n\n💡 Si tiene dudas sobre cómo subir los documentos, pregúnteme y le ayudo.",
                "pregunta": "¿Entendió lo que debe hacer después del registro?",
                "opciones": ["✅ Sí, entendí", "No, aún tengo dudas"],
                "respuesta_no": {
                    "mensaje": "📌 No se preocupe, aquí le explico con más detalle:\n\n📌 PASO 1: SUBIR DOCUMENTOS AL PORTAL\n- Ingrese a https://proveedores.uniminuto.edu\n- Inicie sesión con su usuario y contraseña.\n- Busque la sección 'Documentos' o 'Subir documentos'.\n- Seleccione cada documento y súbalo.\n- Asegúrese de que estén en PDF y sin contraseña.\n\n📌 PASO 2: RADICAR DOCUMENTOS POR CORREO\n- Envíe los mismos documentos al correo de su supervisor.\n- Si no tiene el correo, escriba al área de contratación.\n- Incluya su nombre y cédula en el asunto del correo.\n\n📌 PASO 3: ESPERAR LA VALIDACIÓN\n- La revisión puede tardar de 1 a 3 días hábiles.\n- Revise su correo (incluyendo spam) periódicamente.\n- Si hay errores, corríjalos y reenvíe los documentos.\n\n📌 PASO 4: FIRMAR EL CONTRATO\n- Después de la aprobación, recibirá el contrato por correo.\n- Lea todo el contrato antes de firmar.\n- Firme digitalmente siguiendo las instrucciones.\n- Guarde una copia del contrato firmado.\n\n💡 Si tiene dudas sobre algún paso, pregúnteme y le explico con más detalle."
                }
            },
            # ===== PASO DE AYUDA EXTERNA (justo antes del final) =====
            {
                "id": "ayuda_externa",
                "titulo": "📌 ¿Sigues teniendo dudas?",
                "contenido": "Si aún tienes dudas sobre el registro en el portal, te recomiendo ver este tutorial:\n\n🔗 https://uniminuto0-my.sharepoint.com/personal/coord_admin_rv_uniminuto_edu/_layouts/15/stream.aspx?id=%2Fpersonal%2Fcoord%5Fadmin%5Frv%5Funiminuto%5Fedu%2FDocuments%2FDAF%2FVARIOS%2FPLANTILLAS%20IMPORTANTES%2FProceso%20para%20Registro%20en%20Plataforma%2D20260223%5F170351%2DGrabaci%C3%B3n%20de%20la%20reuni%C3%B3n%2Emp4&referrer=StreamWebApp%2EWeb&referrerScenario=AddressBarCopied%2Eview%2E44292558%2D9973%2D4a2a%2D9769%2D5a5d1fa63ef1&ct=1785532073546&or=OWA%2DNT%2DMail&cid=dd0a5fe8%2D1ba6%2D696c%2D0456%2Dc616eff8828f&ga=1&LOF=1\n\nSi después de ver el tutorial sigues con problemas, por favor comunícate con tu supervisor para recibir asistencia personalizada.\n\nNo te preocupes, es normal tener dudas. Tu supervisor está ahí para ayudarte.\n\n💡 Para continuar, escribe \"menú\" para volver al inicio.",
                "detalle": "Este paso cierra la ayuda del chatbot y te redirige a tu supervisor o a un tutorial en SharePoint.",
                "pregunta": "¿Listo para continuar?",
                "opciones": ["🏠 Volver al inicio"]  # <--- CAMBIO AQUÍ
            }
        ],
        "final": {
            "mensaje": "🎉 ¡Ya completaste el registro en el portal!\n\nLos siguientes pasos son:\n📋 1. Reunir los documentos requeridos (persona natural o empresa)\n📤 2. Subir los documentos al portal\n📝 3. Firmar el contrato\n\n📌 ¿Qué desea hacer ahora?\n1. Ir al menú principal",
            "opciones": ["🏠 Menú principal"]
        }
    },

    # ============================================================
    # FLUJO: DOCUMENTOS PARA PERSONA NATURAL
    # ============================================================
    "documentos_natural": {
        "nombre": "Documentos para persona natural",
        "descripcion": "Lista de documentos para contratistas independientes",
        "pasos": [
            {
                "id": "intro",
                "titulo": "📋 Documentos para persona natural",
                "contenido": "Para contratar como persona natural necesita presentar estos 6 documentos:\n\n1. 📄 Cédula de ciudadanía (ambas caras)\n2. 🏦 Certificación bancaria (máx. 30 días)\n3. 📋 RUT actualizado (máx. 30 días)\n4. 📊 Formato Excel 'Ingreso Independientes'\n5. 🏥 Certificación ARL activa\n6. 🏥 Examen médico (máx. 3 años)",
                "detalle": "Todos los documentos deben estar en PDF y sin contraseña. Los plazos: certificación bancaria y RUT deben tener menos de 30 días; el examen médico menos de 3 años.",
                "pregunta": "¿Cuál de estos documentos necesita ayuda para obtener?",
                "opciones": ["1. Cédula", "2. Certificación bancaria", "3. RUT", "4. Formato Excel", "5. ARL", "6. Examen médico", "🔙 Volver al menú"],
                "respuesta_no": {
                    "mensaje": "📌 Si no entiende algún documento, aquí tiene más información:\n\n1. Cédula: documento de identidad (ambas caras en PDF).\n2. Certificación bancaria: documento del banco que confirma su cuenta.\n3. RUT: registro tributario de la DIAN (menos de 30 días).\n4. Formato Excel: archivo que debe diligenciar con sus datos.\n5. ARL: afiliación a riesgos laborales.\n6. Examen médico: certificado de salud ocupacional.\n\nTodos en PDF y sin contraseña."
                }
            },
            {
                "id": "cedula",
                "titulo": "📄 Cédula de ciudadanía",
                "contenido": "📌 ¿CÓMO OBTENERLA?\n- Escanee ambas caras en un solo PDF\n- Asegúrese de que se vean claramente todos los datos\n- En PDF y sin contraseña\n- También sirve cédula de extranjería",
                "detalle": "Si su cédula está deteriorada, solicite una copia auténtica en la Registraduría. Si tiene cédula de extranjería, verifique que tenga permiso de trabajo vigente.",
                "pregunta": "¿Ya tiene su cédula lista o necesita ayuda para escanearla?",
                "opciones": ["✅ Ya la tengo lista", "📸 Necesito ayuda para escanearla", "🔙 Volver a documentos"],
                "respuesta_no": {
                    "mensaje": "📸 Si necesita ayuda para escanear su cédula:\n\n1. Use el escáner de su impresora o una app de escaneo (Adobe Scan, CamScanner).\n2. Escanee ambas caras en un solo archivo PDF.\n3. Asegúrese de que la imagen sea clara y se vean todos los datos.\n4. El PDF no debe tener contraseña.\n5. Si no tiene escáner, puede tomarle una foto clara con su celular y convertirla a PDF.\n\n✅ Si ya tiene su cédula lista, seleccione 'Ya la tengo lista'."
                }
            },
            {
                "id": "cert_bancaria",
                "titulo": "🏦 Certificación bancaria",
                "contenido": "📌 ¿CÓMO OBTENERLA?\n- Solicítela en su banco (app, web o sucursal)\n- Fecha de expedición NO mayor a 30 días\n- Debe estar a su nombre (igual al RUT)\n- Formato PDF sin contraseña",
                "detalle": "Puede pedirla por la banca en línea, es más rápido. Bancos: Davivienda, Bancolombia, BBVA, Banco de Bogotá, Caja Social, Nequi, Daviplata, Lulo Bank, Nu Bank.",
                "pregunta": "¿Ya tiene su certificación bancaria lista?",
                "opciones": ["✅ Ya la tengo lista", "📄 Necesito pedirla", "🔙 Volver a documentos"],
                "respuesta_no": {
                    "mensaje": "📄 Si necesita pedir la certificación bancaria:\n\n1. Ingrese a la app o página web de su banco.\n2. Busque la opción 'Certificaciones' o 'Certificado de cuenta'.\n3. Solicite la certificación bancaria a su nombre.\n4. La fecha de expedición debe ser menor a 30 días.\n5. Descárguela en PDF (sin contraseña).\n6. Si no puede pedirla por la app, vaya a una sucursal física.\n\n💡 Puede hacerlo en: Davivienda, Bancolombia, BBVA, Banco de Bogotá, Caja Social, Nequi, Daviplata, Lulo Bank, Nu Bank."
                }
            },
            {
                "id": "rut",
                "titulo": "📋 RUT actualizado",
                "contenido": "📌 REQUISITOS DEL RUT:\n- Fecha de expedición: menor a 30 días\n- Marca de agua: 'Copia' o 'Certificado'\n- NO 'En trámite' ni 'Borrador'\n- Actividad económica: 8560 es recomendada",
                "detalle": "Si su RUT dice 'En trámite', debe esperar a que la DIAN lo apruebe (24-72 horas). Para actualizarlo, ingrese a www.dian.gov.co y busque 'Actualización RUT'.",
                "pregunta": "¿Su RUT cumple con estos requisitos?",
                "opciones": ["✅ Sí, ya lo tengo", "🔄 Necesito actualizarlo", "🔙 Volver a documentos"],
                "respuesta_no": {
                    "mensaje": "🔄 Si necesita actualizar su RUT:\n\n1. Ingrese a la DIAN: www.dian.gov.co\n2. Inicie sesión con su usuario y contraseña.\n3. Busque la opción 'Actualización RUT'.\n4. Revise que sus datos estén correctos (dirección, correo, actividad económica).\n5. Actividad económica recomendada: código 8560 (apoyo a la educación).\n6. Descargue el RUT con marca de agua 'Copia' o 'Certificado'.\n7. Verifique que la fecha de expedición sea menor a 30 días.\n\n⚠️ Si su RUT dice 'En trámite', NO sirve. Espere a que la DIAN lo apruebe.\n\n¿Necesita ayuda con algún paso específico?"
                }
            },
            {
                "id": "formato_excel",
                "titulo": "📊 Formato Excel 'Ingreso Independientes'",
                "contenido": "📌 ¿CÓMO DILIGENCIARLO?\n- Abra el archivo que recibió por correo\n- Complete: nombre, cédula, dirección, teléfono, correo\n- Guarde con su nombre y cédula",
                "detalle": "Si no tiene el formato, pídalo en el chat y se lo proporciono. No deje campos obligatorios en blanco.",
                "pregunta": "¿Ya tiene el formato diligenciado?",
                "opciones": ["✅ Sí, ya lo tengo", "📩 Necesito el formato", "🔙 Volver a documentos"],
                "respuesta_no": {
                    "mensaje": "📩 Si necesita el formato Excel:\n\n1. El formato se llama 'Ingreso Independientes'.\n2. Debe haberlo recibido por correo electrónico cuando inició el proceso.\n3. Complete todos los campos: nombre, cédula, dirección, teléfono, correo.\n4. Guarde el archivo con su nombre y cédula (ej: JuanPerez_12345678.xlsx).\n\n📌 Si no tiene el formato, puedo enviárselo al chat. Escríbame y se lo proporciono."
                }
            },
            {
                "id": "arl",
                "titulo": "🏥 Certificación ARL",
                "contenido": "📌 ¿CÓMO OBTENERLA?\n- Comuníquese con su ARL\n- Solicite certificación de afiliación\n- Debe estar activa como trabajador independiente\n- Formato PDF sin contraseña\n\nARL RECOMENDADAS: Positiva, Sura, Colmena, AXA Colpatria, Seguros Bolívar, La Equidad",
                "detalle": "Si no tiene ARL, comuníquese con una de las ARL recomendadas y solicite su afiliación como trabajador independiente. Tiene un costo mensual.",
                "pregunta": "¿Ya tiene ARL activa o necesita ayuda para afiliarse?",
                "opciones": ["✅ Ya tengo ARL", "🆘 Necesito afiliarme", "🔙 Volver a documentos"],
                "respuesta_no": {
                    "mensaje": "🆘 Si necesita afiliarse a una ARL:\n\n1. Elija una ARL de la lista recomendada, 💡 Puede elegir la ARL de su preferencia. Todas son válidas.:\n   - Positiva\n   - Sura\n   - Colmena\n   - AXA Colpatria\n   - Seguros Bolívar\n   - La Equidad\n\n2. Comuníquese con la ARL elegida.\n3. Solicite afiliación como trabajador independiente.\n4. Indique que necesita la certificación para contratar con UNIMINUTO.\n5. La afiliación tiene un costo mensual.\n6. Solicite la certificación en PDF sin contraseña.\n\n💡 La certificación debe ser reciente (menos de 30 días)."
                }
            },
            {
                "id": "examen_medico",
                "titulo": "🏥 Examen médico ocupacional",
                "contenido": "📌 REQUISITOS:\n- Vigencia máxima de 3 años\n- Debe indicar que es APTO para el cargo\n- Realícelo en ARL, clínica ocupacional o IPS autorizada\n- Costo: depende de la entidad y los exámenes requeridos",
                "detalle": "Si no sabe dónde hacerlo, consulte con su ARL o con el área de talento humano de UNIMINUTO Virtual. Si su examen tiene más de 3 años, debe renovarlo.",
                "pregunta": "¿Ya tiene su examen médico al día?",
                "opciones": ["✅ Sí, lo tengo", "📍 Necesito dónde hacerlo", "🔙 Volver a documentos"],
                "respuesta_no": {
                    "mensaje": "📍 Si necesita hacer el examen médico:\n\n1. Puede realizarlo en:\n   - ARL (Administradora de Riesgos Laborales)\n   - Clínicas ocupacionales\n   - IPS autorizadas\n\n2. Pida una cita para examen médico ocupacional.\n3. El certificado debe indicar que es APTO para el cargo.\n4. Costo aproximado: depende de la entidad.\n5. Solicite el certificado en PDF sin contraseña.\n\n💡 Consulte con su ARL, a veces cubren el examen.\nSi no sabe dónde hacerlo, consulte con su ARL o con el área de talento humano de UNIMINUTO Virtual."
                }
            },
            # ===== PASO DE AYUDA EXTERNA (justo antes del final) =====
            {
                "id": "ayuda_externa",
                "titulo": "📌 ¿Sigues teniendo dudas?",
                "contenido": "Si aún tienes dudas sobre los documentos requeridos, te recomiendo ver este tutorial:\n\n🔗 https://uniminuto0-my.sharepoint.com/personal/coord_admin_rv_uniminuto_edu/_layouts/15/stream.aspx?id=%2Fpersonal%2Fcoord%5Fadmin%5Frv%5Funiminuto%5Fedu%2FDocuments%2FDAF%2FVARIOS%2FPLANTILLAS%20IMPORTANTES%2FProceso%20para%20Registro%20en%20Plataforma%2D20260223%5F170351%2DGrabaci%C3%B3n%20de%20la%20reuni%C3%B3n%2Emp4&referrer=StreamWebApp%2EWeb&referrerScenario=AddressBarCopied%2Eview%2E44292558%2D9973%2D4a2a%2D9769%2D5a5d1fa63ef1&ct=1785532073546&or=OWA%2DNT%2DMail&cid=dd0a5fe8%2D1ba6%2D696c%2D0456%2Dc616eff8828f&ga=1&LOF=1\n\nSi después de ver el tutorial sigues con problemas, por favor comunícate con tu supervisor para recibir asistencia personalizada.\n\nNo te preocupes, es normal tener dudas. Tu supervisor está ahí para ayudarte.\n\n💡 Para continuar, escribe \"menú\" para volver al inicio.",
                "detalle": "Este paso cierra la ayuda del chatbot y te redirige a tu supervisor o a un tutorial en SharePoint.",
                "pregunta": "¿Listo para continuar?",
                "opciones": ["🏠 Volver al inicio"]  # <--- CAMBIO AQUÍ
            }
        ],
        "final": {
            "mensaje": "✅ Ya revisamos todos los documentos para persona natural.\n\nRecuerde:\n- 📄 Cédula (ambas caras, PDF)\n- 🏦 Certificación bancaria (30 días, PDF)\n- 📋 RUT actualizado (30 días, PDF)\n- 📊 Formato Excel\n- 🏥 ARL activa\n- 🏥 Examen médico (3 años)\n\n📌 ¿Qué desea hacer ahora?\n1. Ir al menú principal",
            "opciones": ["🏠 Menú principal"]
        }
    },

    # ============================================================
    # FLUJO: ACTUALIZACIÓN DEL RUT
    # ============================================================
    "rut_actualizar": {
        "nombre": "Actualización del RUT",
        "descripcion": "Pasos para actualizar el RUT en la DIAN",
        "pasos": [
            {
                "id": "paso_1",
                "titulo": "PASO 1: Acceder a la DIAN",
                "contenido": "🔹 Abra su navegador (Chrome o Firefox)\n🔹 Vaya a: www.dian.gov.co\n🔹 Haga clic en 'Iniciar sesión'",
                "detalle": "Si no tiene usuario en la DIAN, debe crearlo seleccionando 'Registrarse' o 'Crear usuario'. Si olvidó su contraseña, use la opción 'Recuperar contraseña'.",
                "pregunta": "¿Ya pudo acceder a la DIAN?",
                "opciones": ["✅ Sí, ya ingresé", "🔐 No tengo usuario", "🔙 Volver al menú"],
                "respuesta_no": {
                    "mensaje": "🔐 Si no tiene usuario en la DIAN:\n\n1. Vaya a www.dian.gov.co\n2. Haga clic en 'Registrarse' o 'Crear usuario'.\n3. Complete el formulario con sus datos personales.\n4. Confirme su correo electrónico.\n5. Espere la activación de su cuenta.\n\n🔐 Si olvidó su contraseña:\n1. Haga clic en '¿Olvidó su contraseña?'.\n2. Ingrese su usuario y correo.\n3. Siga las instrucciones para recuperarla.\n\n💡 El proceso es gratuito y no necesita ir a una oficina."
                }
            },
            {
                "id": "paso_2",
                "titulo": "PASO 2: Buscar Actualización RUT",
                "contenido": "🔹 En el menú principal, busque 'Actualización RUT'\n🔹 Está en 'Servicios en línea' o 'Trámites'",
                "detalle": "Si no encuentra la opción, busque 'Actualización de datos' o 'Registro Único Tributario'. La DIAN a veces cambia la ubicación de los menús.",
                "pregunta": "¿Ya encontró la opción 'Actualización RUT'?",
                "opciones": ["✅ Sí, ya la encontré", "🔍 No la encuentro", "🔙 Volver al menú"],
                "respuesta_no": {
                    "mensaje": "🔍 Si no encuentra la opción 'Actualización RUT':\n\n1. Asegúrese de estar en el menú principal de la DIAN.\n2. Busque en 'Servicios en línea' o 'Trámites'.\n3. También puede buscar 'Actualización de datos' o 'Registro Único Tributario'.\n4. Si no la encuentra, use el buscador de la página.\n5. Si sigue sin encontrarla, intente con otro navegador.\n\n💡 La DIAN a veces cambia la ubicación de los menús. No se desanime."
                }
            },
            {
                "id": "paso_3",
                "titulo": "PASO 3: Revisar y actualizar datos",
                "contenido": "🔹 Verifique que sus datos estén correctos:\n- Dirección de residencia\n- Correo electrónico\n- Teléfono\n- Actividad económica\n\n🔹 Actividad recomendada: código 8560 (apoyo a la educación)",
                "detalle": "La actividad económica debe ser REAL. No la invente. 8560 es una RECOMENDACIÓN, no una obligación. Si tiene otra actividad, use el código que corresponda.",
                "pregunta": "¿Ya revisó y actualizó sus datos?",
                "opciones": ["✅ Ya los revisé", "📋 Necesito ayuda con la actividad", "🔙 Volver al menú"],
                "respuesta_no": {
                    "mensaje": "📋 Si necesita ayuda con la actividad económica:\n\n1. La actividad económica es el código que describe su labor.\n2. Si trabaja en educación, use el código 8560 (recomendado).\n3. Si tiene otra profesión, use el código que corresponda.\n   - 8530 → Educación (para profesores)\n   - 7020 → Consultoría\n   - 7410 → Diseño\n   - 6201 → Desarrollo de software\n\n4. La actividad debe ser REAL. No la invente.\n5. Si no está seguro, consulte con su contador.\n\n💡 8560 es una RECOMENDACIÓN, no una obligación."
                }
            },
            {
                "id": "paso_4",
                "titulo": "PASO 4: Descargar el RUT actualizado",
                "contenido": "🔹 Busque la opción 'Descargar RUT'\n🔹 Seleccione la marca de agua 'Copia' o 'Certificado'\n🔹 NUNCA descargue la versión 'En trámite'",
                "detalle": "Si su RUT dice 'En trámite', NO es válido. Debe esperar a que la DIAN lo apruebe (24-72 horas). La marca de agua debe decir 'Copia' o 'Certificado'.",
                "pregunta": "¿Ya descargó su RUT actualizado?",
                "opciones": ["✅ Sí, ya lo descargué", "⏳ Está en trámite", "🔙 Volver al menú"],
                "respuesta_no": {
                    "mensaje": "⏳ Si su RUT dice 'En trámite':\n\n1. NO es válido para contratar con UNIMINUTO.\n2. Debe esperar a que la DIAN lo apruebe (24-72 horas hábiles).\n3. Después de aprobado, descargue el RUT nuevamente.\n4. Asegúrese de que la marca de agua sea 'Copia' o 'Certificado'.\n\n💡 Si pasa más de 72 horas, comuníquese con la DIAN.\n\n✅ Cuando esté listo, descárguelo y verifique que cumpla con los requisitos."
                }
            },
            {
                "id": "paso_5",
                "titulo": "PASO 5: Verificar el documento",
                "contenido": "🔹 Revise que su nuevo RUT tenga:\n- ✅ Fecha de expedición menor a 30 días\n- ✅ Marca de agua: 'Copia' o 'Certificado'\n- ✅ Su nombre y cédula correctos\n- ✅ Actividad económica correcta",
                "detalle": "Si todo está correcto, su RUT ya está listo para subir al portal. Si algo falla, repita el proceso o consulte con un contador.",
                "pregunta": "¿Su RUT ya está listo para usar?",
                "opciones": ["✅ Sí, ya está listo", "🔄 No, algo falló", "🔙 Volver al menú"],
                "respuesta_no": {
                    "mensaje": "🔄 Si algo falló en su RUT:\n\n1. Revise la fecha de expedición: debe ser menor a 30 días.\n2. Revise la marca de agua: debe ser 'Copia' o 'Certificado'.\n3. Verifique que su nombre y cédula estén correctos.\n4. Verifique la actividad económica.\n\nSi algún dato está incorrecto:\n1. Vuelva a la DIAN.\n2. Actualice los datos necesarios.\n3. Descargue un nuevo RUT.\n\n💡 Si tiene dudas, consulte con un contador."
                }
            },
            # ===== PASO DE AYUDA EXTERNA (justo antes del final) =====
            {
                "id": "ayuda_externa",
                "titulo": "📌 ¿Sigues teniendo dudas?",
                "contenido": "Si aún tienes dudas sobre la actualización del RUT, te recomiendo ver este tutorial en YouTube:\n\n🔗 https://www.youtube.com/watch?v=bbZbULl1l8Y\n\nSi después de ver el tutorial sigues con problemas, por favor comunícate con tu supervisor para recibir asistencia personalizada.\n\nNo te preocupes, es normal tener dudas. Tu supervisor está ahí para ayudarte.\n\n💡 Para continuar, escribe \"menú\" para volver al inicio.",
                "detalle": "Este paso cierra la ayuda del chatbot y te redirige a tu supervisor o a un tutorial en YouTube.",
                "pregunta": "¿Listo para continuar?",
                "opciones": ["🏠 Volver al inicio"]  # <--- CAMBIO AQUÍ
            }
        ],
        "final": {
            "mensaje": "✅ ¡Tu RUT ya está actualizado!\n\nRecuerda:\n- 📅 Fecha de expedición: menor a 30 días\n- 💧 Marca de agua: 'Copia' o 'Certificado'\n- 📋 Actividad económica: 8560 (recomendada)\n\n📌 ¿Qué desea hacer ahora?\n1. Ir a documentos\n2. Ir al registro en portal\n3. Ir al menú principal",
            "opciones": ["📋 Documentos", "🌐 Registro en portal", "🏠 Menú principal"]
        }
    },

    # ============================================================
    # FLUJO: ARL
    # ============================================================
    "arl": {
        "nombre": "ARL - Afiliación y certificación",
        "descripcion": "Guía para afiliarse a una ARL y obtener la certificación",
        "pasos": [
            {
                "id": "intro",
                "titulo": "🏥 ¿Qué es la ARL?",
                "contenido": "La ARL (Administradora de Riesgos Laborales) protege a los trabajadores contra accidentes y enfermedades relacionadas con su trabajo.\n\n🔹 ES OBLIGATORIA para todos los contratistas de UNIMINUTO.",
                "detalle": "Sin ARL activa, no puede contratar con UNIMINUTO. Debe afiliarse antes de iniciar el proceso.",
                "pregunta": "¿Ya tiene ARL o necesita afiliarse?",
                "opciones": ["✅ Ya tengo ARL", "🆘 Necesito afiliarme", "🔙 Volver al menú"],
                "respuesta_no": {
                    "mensaje": "🆘 Si necesita afiliarse a una ARL:\n\n1. Elija una ARL de la lista recomendada:\n   - Positiva\n   - Sura\n   - Colmena\n   - AXA Colpatria\n   - Seguros Bolívar\n   - La Equidad\n\n2. Comuníquese con la ARL elegida.\n3. Solicite afiliación como trabajador independiente.\n4. Indique que necesita la certificación para contratar con UNIMINUTO.\n5. La afiliación tiene un costo mensual.\n6. Solicite la certificación en PDF sin contraseña.\n\n💡 La certificación debe ser reciente (menos de 30 días)."
                }
            },
            {
                "id": "afiliacion",
                "titulo": "🆘 Cómo afiliarse a una ARL",
                "contenido": "🔹 PASO 1: Elija una ARL\n- Positiva\n- Sura\n- Colmena\n- AXA Colpatria\n- Seguros Bolívar\n- La Equidad\n💡 Puede elegir la ARL de su preferencia. Todas son válidas.\n\n🔹 PASO 2: Reúna los documentos\n- Cédula\n- RUT (si tiene)\n- Información de contacto",
                "detalle": "Contacte la ARL de su elección, pida afiliación como trabajador independiente e indique que necesita la certificación para contratar con UNIMINUTO.",
                "pregunta": "¿Ya eligió una ARL o necesita ayuda para decidir?",
                "opciones": ["✅ Ya elegí una", "📞 Ayúdeme a elegir", "🔙 Volver al menú"],
                "respuesta_no": {
                    "mensaje": "📞 Aquí tiene información para elegir una ARL:\n\n1. Positiva: https://www.positiva.gov.co\n2. Sura: https://www.sura.com\n3. Colmena: https://www.colmena.com\n4. AXA Colpatria: https://www.axa.com.co\n5. Seguros Bolívar: https://www.segurosbolivar.com\n6. La Equidad: https://www.laequidad.com\n\n💡 Todas estas ARL ofrecen afiliación para trabajadores independientes.\nElija la que mejor se adapte a sus necesidades."
                }
            },
            {
                "id": "certificacion",
                "titulo": "📄 Certificación de ARL",
                "contenido": "🔹 Una vez afiliado, solicite la certificación\n🔹 Debe estar en formato PDF\n🔹 En PDF y sin contraseña\n🔹 Debe ser reciente (no mayor a 30 días)",
                "detalle": "La certificación es gratuita después de la afiliación. Pregunte por el costo mensual de la afiliación como independiente.",
                "pregunta": "¿Ya tiene su certificación de ARL lista?",
                "opciones": ["✅ Sí, ya la tengo", "📄 Necesito pedirla", "🔙 Volver al menú"],
                "respuesta_no": {
                    "mensaje": "📄 Si necesita pedir la certificación de ARL:\n\n1. Comuníquese con su ARL (por teléfono, correo o portal).\n2. Solicite la certificación de afiliación.\n3. Indique que la necesita para contratar con UNIMINUTO.\n4. Solicítela en formato PDF sin contraseña.\n5. Verifique que la fecha sea reciente (menos de 30 días).\n\n💡 La certificación es gratuita después de la afiliación."
                }
            },
            # ===== PASO DE AYUDA EXTERNA (justo antes del final) =====
            {
                "id": "ayuda_externa",
                "titulo": "📌 ¿Sigues teniendo dudas?",
                "contenido": "Si aún tienes dudas sobre la ARL, te recomiendo ver este tutorial en YouTube:\n\n🔗 https://youtu.be/S-ps-ctVbAU?si=mTQZH4p9SGvYmWr9\n\nSi después de ver el tutorial sigues con problemas, por favor comunícate con tu supervisor para recibir asistencia personalizada.\n\nNo te preocupes, es normal tener dudas. Tu supervisor está ahí para ayudarte.\n\n💡 Para continuar, escribe \"menú\" para volver al inicio.",
                "detalle": "Este paso cierra la ayuda del chatbot y te redirige a tu supervisor o a un tutorial en YouTube.",
                "pregunta": "¿Listo para continuar?",
                "opciones": ["🏠 Volver al inicio"]  # <--- CAMBIO AQUÍ
            }
        ],
        "final": {
            "mensaje": "✅ ¡Ya tienes tu ARL lista!\n\nRecuerda:\n- 🏥 ARL activa como trabajador independiente\n- 📄 Certificación en PDF sin contraseña\n- 📅 Fecha reciente (menos de 30 días)\n\n📌 ¿Qué desea hacer ahora?\n1. Ir a documentos\n2. Ir al registro en portal\n3. Ir al menú principal",
            "opciones": ["📋 Documentos", "🌐 Registro en portal", "🏠 Menú principal"]
        }
    },

    # ============================================================
    # FLUJO: EXAMEN MÉDICO
    # ============================================================
    "examen_medico": {
        "nombre": "Examen médico ocupacional",
        "descripcion": "Guía para obtener el examen médico",
        "pasos": [
            {
                "id": "intro",
                "titulo": "🏥 Examen médico ocupacional",
                "contenido": "El examen médico ocupacional evalúa su condición física y mental para desempeñar el cargo.\n\n🔹 ES OBLIGATORIO para todos los contratistas\n🔹 Vigencia máxima: 3 años",
                "detalle": "Si su examen tiene más de 3 años, debe renovarlo. No puede omitirlo.",
                "pregunta": "¿Ya tiene examen médico o necesita hacerlo?",
                "opciones": ["✅ Ya lo tengo", "📍 Necesito hacerlo", "🔙 Volver al menú"],
                "respuesta_no": {
                    "mensaje": "📍 Si necesita hacer el examen médico:\n\n1. Puede realizarlo en:\n   - ARL (Administradora de Riesgos Laborales)\n   - Clínicas ocupacionales\n   - IPS autorizadas\n\n2. Pida una cita para examen médico ocupacional.\n3. El certificado debe indicar que es APTO para el cargo.\n4. Costo aproximado: depende de la entidad.\n5. Solicite el certificado en PDF sin contraseña.\n\n💡 Consulte con su ARL, a veces cubren el examen.\nSi no sabe dónde hacerlo, consulte con su ARL o con el área de talento humano de UNIMINUTO Virtual."
                }
            },
            {
                "id": "donde",
                "titulo": "📍 Dónde hacer el examen médico",
                "contenido": "Puede realizarlo en:\n- 🏥 ARL (Administradora de Riesgos Laborales)\n- 🏥 Clínicas ocupacionales\n- 🏥 IPS autorizadas\n\n🔹 Costo: depende de la entidad y los exámenes requeridos",
                "detalle": "Consulte con su ARL, a veces cubren el examen. Pida cita para examen médico ocupacional y solicite el certificado en PDF.",
                "pregunta": "¿Ya sabe dónde va a hacerlo?",
                "opciones": ["✅ Sí, ya sé dónde", "🔍 Ayúdeme a encontrar", "🔙 Volver al menú"],
                "respuesta_no": {
                    "mensaje": "🔍 Si no sabe dónde hacer el examen médico:\n\n1. Consulte con su ARL (Administradora de Riesgos Laborales).\n2. Pregunte si cubren el examen o si tienen convenios con clínicas.\n3. Busque clínicas ocupacionales en su ciudad.\n4. Pregunte a su supervisor de UNIMINUTO si conoce algún lugar.\n\n💡 También puede buscar en Google: 'examen médico ocupacional [su ciudad]'.\n\nUna vez que sepa dónde hacerlo, pida una cita y solicite el certificado en PDF."
                }
            },
            {
                "id": "resultado",
                "titulo": "📄 Resultado del examen",
                "contenido": "🔹 El certificado debe indicar que es APTO para el cargo\n🔹 Formato PDF sin contraseña\n🔹 Vigencia máxima de 3 años",
                "detalle": "Si el examen dice 'Apto con restricciones', consulte con su supervisor si es válido. En la mayoría de los casos debe ser 'Apto' sin restricciones.",
                "pregunta": "¿Ya tiene su resultado en PDF?",
                "opciones": ["✅ Sí, ya lo tengo", "⏳ Estoy esperando el resultado", "🔙 Volver al menú"],
                "respuesta_no": {
                    "mensaje": "⏳ Si está esperando el resultado de su examen médico:\n\n1. Los resultados suelen tardar de 1 a 3 días hábiles.\n2. Consulte con la clínica o IPS donde se realizó el examen.\n3. Pregunte si el certificado se puede entregar en PDF.\n4. Asegúrese de que diga APTO para el cargo.\n5. Vigencia: 3 años.\n\n💡 Si el resultado dice 'Apto con restricciones', consulte con su supervisor."
                }
            },
            # ===== PASO DE AYUDA EXTERNA (justo antes del final) =====
            {
                "id": "ayuda_externa",
                "titulo": "📌 ¿Sigues teniendo dudas?",
                "contenido": "Si aún tienes dudas sobre el examen médico, te recomiendo ver este tutorial en YouTube:\n\n🔗 [LINK_EXAMEN_MEDICO_PENDIENTE]\n\nSi después de ver el tutorial sigues con problemas, por favor comunícate con tu supervisor para recibir asistencia personalizada.\n\nNo te preocupes, es normal tener dudas. Tu supervisor está ahí para ayudarte.\n\n💡 Para continuar, escribe \"menú\" para volver al inicio.",
                "detalle": "Este paso cierra la ayuda del chatbot y te redirige a tu supervisor o a un tutorial en YouTube.",
                "pregunta": "¿Listo para continuar?",
                "opciones": ["🏠 Volver al inicio"]  # <--- CAMBIO AQUÍ
            }
        ],
        "final": {
            "mensaje": "✅ ¡Ya tienes tu examen médico listo!\n\nRecuerda:\n- 🏥 APTO para el cargo\n- 📄 PDF sin contraseña\n- 📅 Vigencia: 3 años\n\n📌 ¿Qué desea hacer ahora?\n1. Ir a documentos\n2. Ir al registro en portal\n3. Ir al menú principal",
            "opciones": ["📋 Documentos", "🌐 Registro en portal", "🏠 Menú principal"]
        }
    },
}

# ============================================================
# FUNCIONES DE AYUDA PARA ACCEDER A LOS FLUJOS
# ============================================================

def obtener_flujo(flujo_id):
    """Obtiene un flujo por su ID"""
    return FLUJOS.get(flujo_id)

def obtener_paso(flujo_id, indice):
    """Obtiene un paso específico de un flujo"""
    flujo = obtener_flujo(flujo_id)
    if not flujo:
        return None
    pasos = flujo.get('pasos', [])
    if 0 <= indice < len(pasos):
        return pasos[indice]
    return None

def total_pasos(flujo_id):
    """Obtiene el número total de pasos de un flujo"""
    flujo = obtener_flujo(flujo_id)
    if not flujo:
        return 0
    return len(flujo.get('pasos', []))

def es_paso_final(flujo_id, indice):
    """Verifica si un índice es el último paso del flujo"""
    return indice >= total_pasos(flujo_id) - 1

def obtener_titulo_flujo(flujo_id):
    """Obtiene el título de un flujo"""
    flujo = obtener_flujo(flujo_id)
    if not flujo:
        return "Tema"
    return flujo.get('nombre', 'Tema')

def obtener_mensaje_final(flujo_id):
    """Obtiene el mensaje final de un flujo"""
    flujo = obtener_flujo(flujo_id)
    if not flujo:
        return None
    return flujo.get('final', {}).get('mensaje', '')