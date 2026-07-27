
# chatbot/conocimiento/contratos.py
"""
Base de conocimiento sobre CONTRATOS
Todas las preguntas y respuestas sobre contratos, firma, condiciones, etc.
"""

# ============================================================
# PATRONES PARA DETECTAR PREGUNTAS DE CONTRATOS
# ============================================================

PATRONES_CONTRATOS = [
    # Generales
    "contrato", "contratacion", "contratación", "firma de contrato", "firmar contrato",
    "que es un contrato", "tipos de contrato", "contrato de prestacion de servicios",
    "contrato laboral", "contrato civil", "contrato comercial",
    
    # Firma
    "como firmo el contrato", "firma digital", "firmar digitalmente", "donde firmo",
    "no puedo firmar", "problemas para firmar", "firma electronica",
    
    # Condiciones
    "condiciones del contrato", "clausulas del contrato", "terminos y condiciones",
    "objeto del contrato", "duracion del contrato", "plazo del contrato",
    
    # Modificaciones
    "modificar contrato", "cambiar contrato", "renovar contrato", "prorroga",
    "extension del contrato", "terminacion del contrato", "terminar contrato",
    
    # Obligaciones
    "obligaciones del contratista", "deberes del contratista", "responsabilidades",
    "entregables", "productos", "resultados esperados",
    
    # Pagos (lo básico)
    "forma de pago", "como me pagan", "cuando me pagan", "pagos del contrato",
    "valor del contrato", "honorarios", "remuneracion",
    
    # Supervisión
    "supervisor del contrato", "quien es mi supervisor", "supervisora",
    "quien me supervisa", "contacto con supervisor",
]

# ============================================================
# RESPUESTAS SOBRE CONTRATOS
# ============================================================

def respuesta_contratos(pregunta):
    """
    Devuelve la respuesta más adecuada para una pregunta sobre contratos
    """
    p = pregunta.lower()
    
    # ============================================================
    # 1. QUÉ ES UN CONTRATO
    # ============================================================
    if any(x in p for x in ['que es un contrato', 'contrato de prestacion', 'que es contratacion', 'contrato laboral']):
        return """📋 ¿QUÉ ES UN CONTRATO DE PRESTACIÓN DE SERVICIOS?

Un contrato de prestación de servicios es un acuerdo legal entre usted (contratista) y UNIMINUTO Virtual, donde usted se compromete a realizar una actividad específica a cambio de una remuneración económica.

🔹 CARACTERÍSTICAS PRINCIPALES:

1. RELACIÓN CIVIL Y COMERCIAL
   - No es un contrato laboral, sino civil o comercial.
   - Usted actúa como un contratista independiente.
   - No tiene relación de subordinación con UNIMINUTO.

2. OBJETO DEL CONTRATO
   - Define exactamente qué actividades va a realizar.
   - Especifica los entregables o productos esperados.
   - Establece los plazos y fechas de entrega.

3. DURACIÓN
   - Puede ser por un tiempo determinado (ej: 6 meses, 1 año).
   - Puede ser por obra o labor determinada.
   - Puede tener prórrogas o renovaciones.

4. REMUNERACIÓN
   - Se establece un valor fijo o por hora.
   - Los pagos se realizan según lo acordado (mensual, por entregas, etc.).
   - Incluye IVA si aplica según su régimen tributario.

5. OBLIGACIONES
   - Usted se compromete a entregar los productos o servicios.
   - UNIMINUTO se compromete a pagar y dar las condiciones para el trabajo.

🔹 DIFERENCIA CON CONTRATO LABORAL:
- Contrato de prestación de servicios: usted es independiente, pone sus propios medios, no tiene horario fijo.
- Contrato laboral: hay subordinación, horario fijo, dependencia.

⚠️ IMPORTANTE:
- Lea TODO el contrato antes de firmarlo.
- Asegúrese de entender cada cláusula.
- Si tiene dudas, pregunte a su supervisor o al área legal.

¿Necesita información sobre algún aspecto específico del contrato?"""

    # ============================================================
    # 2. CÓMO FIRMAR EL CONTRATO
    # ============================================================
    if any(x in p for x in ['como firmo', 'firma digital', 'firmar digitalmente', 'donde firmo', 'no puedo firmar', 'firma electronica']):
        return """📝 CÓMO FIRMAR EL CONTRATO - GUÍA COMPLETA

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

⚠️ PROBLEMAS COMUNES AL FIRMAR:

1. "No me llega el correo"
   - Revise la carpeta de spam.
   - Verifique que su correo sea el correcto.
   - Comuníquese con el área de contratación.

2. "No puedo abrir el enlace"
   - Use Chrome o Firefox actualizados.
   - Intente desde otro navegador.
   - Limpie la caché del navegador.

3. "La firma no se completa"
   - Verifique su conexión a internet.
   - Intente en otro horario.
   - Comuníquese con soporte técnico.

💡 CONSEJO IMPORTANTE:
- Firme dentro del plazo indicado (generalmente 3 a 5 días hábiles).
- Si no firma a tiempo, su proceso puede retrasarse o cancelarse.
- Guarde una copia del contrato firmado para sus registros.

¿Necesita ayuda con algún paso específico?"""

    # ============================================================
    # 3. MODIFICACIONES Y RENOVACIONES
    # ============================================================
    if any(x in p for x in ['modificar contrato', 'cambiar contrato', 'renovar contrato', 'prorroga', 'extension', 'terminacion']):
        return """📋 MODIFICACIONES, RENOVACIONES Y TERMINACIÓN DE CONTRATO

🔹 MODIFICACIÓN DEL CONTRATO (OTROSÍ)
- Si necesita cambiar algún aspecto del contrato (objeto, fechas, valor), se puede hacer mediante un documento llamado "Otrosí".
- Este es un anexo al contrato que modifica cláusulas específicas.
- Debe ser acordado entre ambas partes y firmado nuevamente.
- Procedimiento:
  1. Solicitud formal de modificación a UNIMINUTO.
  2. Análisis y aprobación de la solicitud.
  3. Elaboración y firma del Otrosí.

🔹 RENOVACIÓN DEL CONTRATO (PRÓRROGA)
- Cuando el contrato finaliza y se necesita extender el plazo.
- Puede ser por el mismo objeto o por uno similar.
- Requiere aprobación de su supervisor y del área de contratación.
- Procedimiento:
  1. Evaluación de su desempeño.
  2. Solicitud formal de prórroga.
  3. Aprobación de la prórroga.
  4. Firma del nuevo documento.

🔹 TERMINACIÓN DEL CONTRATO
Puede terminar por varias razones:

1. TERMINACIÓN POR CUMPLIMIENTO
   - Se cumplió el plazo y los entregables.
   - Es la forma más común y natural de terminación.

2. TERMINACIÓN ANTICIPADA
   - Por mutuo acuerdo entre las partes.
   - Por incumplimiento de obligaciones.
   - Por razones de fuerza mayor.

3. TERMINACIÓN POR VOLUNTAD DE UNA PARTE
   - Usted puede renunciar al contrato (con preaviso).
   - UNIMINUTO puede terminar el contrato (con preaviso).

⚠️ PROCESO DE TERMINACIÓN:
1. Notificación formal por escrito.
2. Liquidación de pagos pendientes.
3. Entrega de todos los entregables.
4. Firma de acta de terminación.

💡 RECOMENDACIONES:
- Si necesita modificar o renovar, hágalo con anticipación.
- Revise las fechas de vencimiento de su contrato.
- Comuníquese con su supervisor ante cualquier duda.

¿Necesita información sobre alguna modificación específica?"""

    # ============================================================
    # 4. OBLIGACIONES Y ENTREGABLES
    # ============================================================
    if any(x in p for x in ['obligaciones', 'deberes', 'responsabilidades', 'entregables', 'productos']):
        return """📋 OBLIGACIONES Y ENTREGABLES DEL CONTRATISTA

Como contratista de UNIMINUTO Virtual, usted tiene obligaciones y debe entregar productos específicos. Aquí le explico:

🔹 OBLIGACIONES GENERALES:

1. CUMPLIR CON EL OBJETO DEL CONTRATO
   - Realizar las actividades descritas en el objeto del contrato.
   - No desviarse de lo acordado sin autorización previa.

2. CUMPLIR CON LOS PLAZOS
   - Entregar los productos o servicios en las fechas establecidas.
   - Informar con anticipación si hay algún retraso.

3. CALIDAD DE LOS ENTREGABLES
   - Los productos deben cumplir con los estándares de calidad.
   - Deben ser entregados en el formato especificado.

4. COMUNICACIÓN
   - Responder oportunamente a los mensajes de UNIMINUTO.
   - Informar sobre el avance del trabajo.
   - Notificar cualquier inconveniente.

5. CONFIDENCIALIDAD
   - No compartir información confidencial de UNIMINUTO.
   - Usar la información solo para el objeto del contrato.

🔹 ENTREGABLES COMUNES (ejemplos):
- Documentos técnicos.
- Informes de avance.
- Materiales educativos.
- Cursos virtuales.
- Guiones instruccionales.
- Recursos interactivos.

🔹 CÓMO ENTREGAR:
1. Revise las especificaciones del entregable.
2. Asegúrese de que cumpla con todos los requisitos.
3. Entregue en el formato solicitado (PDF, Word, Excel, etc.).
4. Reciba la confirmación de recepción por parte de UNIMINUTO.

🔹 QUÉ PASA SI NO CUMPLE:
- Su supervisor puede solicitar correcciones.
- El pago puede retrasarse hasta que se completen los entregables.
- Puede afectar futuras contrataciones.

💡 CONSEJOS:
- Pregunte a su supervisor si tiene dudas sobre los entregables.
- Use los formatos y plantillas que le proporcionen.
- Entregue los productos con suficiente anticipación.

¿Necesita ayuda con algún entregable en específico?"""

    # ============================================================
    # 5. PAGOS DEL CONTRATO
    # ============================================================
    if any(x in p for x in ['forma de pago', 'como me pagan', 'cuando me pagan', 'valor del contrato', 'honorarios', 'remuneracion']):
        return """💰 PAGOS DEL CONTRATO - INFORMACIÓN COMPLETA

🔹 FORMAS DE PAGO

1. PAGO ÚNICO
   - Se realiza un solo pago al finalizar el contrato.
   - Ocurre cuando se entregan todos los productos.
   - El pago se efectúa después de la aprobación final.

2. PAGOS MENSUALES
   - Se realiza un pago cada mes.
   - Está asociado a la entrega de avances mensuales.
   - Se debe presentar un informe de avance para cada pago.

3. PAGOS POR ENTREGAS
   - Se paga cada vez que se entrega un hito del proyecto.
   - Los hitos están definidos en el contrato.
   - Cada entrega debe ser aprobada por el supervisor.

🔹 FECHAS DE PAGO
- Los pagos se realizan según lo pactado en el contrato.
- Generalmente son dentro de los 30 días hábiles después de la facturación.
- Consulte su contrato para las fechas específicas.

🔹 REQUISITOS PARA EL PAGO
- Entregar la factura o cuenta de cobro.
- Entregar los productos o servicios acordados.
- Tener la documentación completa.
- Estar al día con las obligaciones tributarias.

🔹 ESTADOS DE FACTURACIÓN
- PTE: Pendiente de pago (aún no se procesa).
- LIBERADO: Listo para pago.
- PAGADO: Ya se realizó el pago.

🔹 PROBLEMAS COMUNES CON EL PAGO
1. "No me han pagado"
   - Verifique el estado en el portal.
   - Confirme que su factura esté correcta.
   - Comuníquese con el área financiera.

2. "Mi factura fue rechazada"
   - Revise que los datos sean correctos.
   - Asegúrese de que tenga todos los requisitos.
   - Corrija y vuelva a presentar la factura.

3. "El pago está demorado"
   - Consulte con su supervisor.
   - Verifique si hay algún problema con su documentación.
   - Comuníquese con el área de pagos.

💡 CONSEJOS PARA RECIBIR SUS PAGOS A TIEMPO:
- Presente sus facturas oportunamente.
- Revise que todos los datos sean correctos.
- Mantenga actualizada su certificación bancaria.
- Confirme con su supervisor que los entregables estén aprobados.

¿Tiene dudas sobre su pago actual?"""

    # ============================================================
    # 6. SUPERVISIÓN DEL CONTRATO
    # ============================================================
    if any(x in p for x in ['supervisor del contrato', 'quien es mi supervisor', 'supervisora', 'quien me supervisa', 'contacto con supervisor']):
        return """👤 SUPERVISIÓN DEL CONTRATO

🔹 ¿QUIÉN ES SU SUPERVISOR?
- Es la persona designada por UNIMINUTO para hacer seguimiento a su contrato.
- Generalmente es su jefe directo o el líder del proyecto.
- Puede ser un profesional, coordinador o director.

🔹 FUNCIONES DEL SUPERVISOR
- Aprobar sus entregables.
- Acompañar y guiar su trabajo.
- Resolver dudas sobre el objeto del contrato.
- Verificar el cumplimiento de plazos.
- Notificar cualquier novedad al área de contratación.

🔹 ¿CÓMO CONTACTAR A SU SUPERVISOR?
1. Por correo electrónico.
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

🔹 CONSEJOS PARA TRABAJAR CON SU SUPERVISOR
- Sea proactivo y comuníquese con frecuencia.
- Cumpla con los plazos acordados.
- Pregunte si tiene dudas (es mejor preguntar que asumir).
- Mantenga un registro de todas las comunicaciones.

⚠️ IMPORTANTE:
- El supervisor es su principal contacto en UNIMINUTO.
- Si tiene problemas con su contrato, hable primero con su supervisor.
- Si el supervisor no resuelve el problema, contacte al área de contratación.

¿Necesita ayuda para contactar a su supervisor?"""

    # ============================================================
    # 7. RESPUESTA POR DEFECTO SOBRE CONTRATOS
    # ============================================================
    return """📋 INFORMACIÓN GENERAL SOBRE CONTRATOS

El contrato de prestación de servicios es el documento que formaliza su relación con UNIMINUTO Virtual.

🔹 ASPECTOS CLAVE DEL CONTRATO:
- Objeto: define qué va a hacer.
- Duración: fechas de inicio y fin.
- Entregables: qué productos debe entregar.
- Valor: cuánto le van a pagar.
- Forma de pago: cómo y cuándo le pagan.
- Supervisor: quién lo supervisa.

🔹 PROCESO DE CONTRATACIÓN:
1. Registro en portal → 2. Entrega de documentos → 3. Validación → 4. Firma → 5. Inicio

🔹 PREGUNTAS FRECUENTES:
- ¿Cómo firmo el contrato? → Le expliqué el proceso de firma digital.
- ¿Cuándo me pagan? → Según lo acordado en el contrato.
- ¿Quién es mi supervisor? → La persona que le asignaron.

🔹 SI TIENE DUDAS ESPECÍFICAS:
- Consulte su contrato.
- Pregunte a su supervisor.
- Comuníquese con el área de contratación.

¿Sobre qué aspecto del contrato necesita más información?"""