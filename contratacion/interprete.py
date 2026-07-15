"""
Intérprete de observaciones y estados - Versión Final
Lenguaje claro para todo tipo de personas
"""

# Mapeo de meses en español
MESES = {
    '01': 'enero', '02': 'febrero', '03': 'marzo', '04': 'abril',
    '05': 'mayo', '06': 'junio', '07': 'julio', '08': 'agosto',
    '09': 'septiembre', '10': 'octubre', '11': 'noviembre', '12': 'diciembre'
}


def formatear_fecha(texto):
    """Convierte fechas tipo 16/06/2026 a 16 de junio de 2026"""
    import re
    patron = r'\b(\d{1,2})[/\-](\d{1,2})[/\-](\d{2,4})\b'
    
    def reemplazar(match):
        dia, mes, anio = match.groups()
        if mes in MESES:
            return f"{dia} de {MESES[mes]} de {anio}"
        return match.group(0)
    
    return re.sub(patron, reemplazar, texto)


def traducir_estado(estado):
    """Traduce el campo ESTADO a lenguaje humano"""
    if not estado:
        return None
    
    e = str(estado).strip()
    
    # Si es NaN o vacío
    if e.lower() in ['nan', 'none', 'null', '']:
        return None
    
    # Casos específicos del estado (los más comunes)
    
    if 'FIRMADO EN CARPETA' in e.upper() or 'CONTRATO FIRMADO EN CARPETA' in e.upper() or 'CONTRATO FIRMADO POR LAS PARTES' in e.upper():
        return '✅ Tu contrato ya está firmado y archivado'
    
    if 'CERRADO' in e.upper() and '23/02' in e:
        return '✅ Proceso cerrado el 23 de febrero de 2026'
    
    if 'CERRADO' in e.upper():
        return '✅ Proceso cerrado'
    
    if 'NO CONTINUA PROCESO' in e.upper() and 'CONTRATISTA DESDE UNIMINUTO' in e.upper():
        return '❌ El proceso no continúa (decisión de UNIMINUTO)'
    
    if 'NO CONTINUA PROCESO' in e.upper() and 'Marzo 26' in e:
        return '❌ El proceso no continúa (decisión del programa)'
    
    if 'NO CONTINUA PROCESO' in e.upper() and 'Mayo 05' in e:
        return '❌ El proceso no continúa (decisión del programa)'
    
    if 'NO CONTINUA PROCESO' in e.upper() or 'NO CONTINÚA PROCESO' in e.upper():
        return '❌ El proceso no continúa'
    
    if 'EXPERTODESISTE' in e.upper() or 'EXPERTO DESISTE' in e.upper():
        return '❌ El experto desistió del contrato'
    
    if 'EN FIRMA DE CONTRATISTA' in e.upper():
        return '📝 El contrato está para tu firma'
    
    if 'CONTRATISTA DESISTE' in e.upper():
        return '❌ El contratista desistió'
    
    if 'SE REMITE PARA FIRMA DEL EXPERTO' in e.upper() or 'SE REMITE PARA  FIRMA DEL EXPERTO' in e.upper():
        return '📝 Tu contrato está para tu firma'
    
    if 'SE REMITE PARA FIRMA DEL RECTOR' in e.upper() or 'SE REMITE PARA FIEMA DEL SEÑOR RECTOR' in e.upper() or 'SE REMITE PARA FIRMA DEL SEÑOR RECTOR' in e.upper():
        return '📝 Contrato para firma del rector'
    
    if 'SE REMITE CONTRATO PARA FIRMA DEL EXPERTRO' in e.upper():
        return '📝 Tu contrato está para tu firma'
    
    if 'SE REMITE CONTRATO PARA FIRMA DEL RECTOR' in e.upper():
        return '📝 Contrato para firma del rector'
    
    if 'SE REMITE CONTRATO PARA FIRMA DEL EXPERTO' in e.upper():
        return '📝 Tu contrato está para tu firma'
    
    if 'PTE ACTA' in e.upper() or 'PENDIENTE ACTA' in e.upper():
        return '⏳ Falta cargar el acta de inicio'
    
    if 'PTE COTIZACION' in e.upper() or 'PENDIENTE COTIZACION' in e.upper() or 'PTE COTIZACIÓN' in e.upper():
        return '⏳ Falta la cotización firmada'
    
    if 'PTE JURIDICA' in e.upper() or 'PDT JURIDICA' in e.upper() or 'PDT AREA JURIDICA' in e.upper():
        return '⏳ En revisión por el área jurídica'
    
    if 'PTE EXAMEN' in e.upper() or 'PENDIENTE EXAMEN' in e.upper():
        return '⏳ Falta el examen médico'
    
    if 'PTE VALIDACION' in e.upper() or 'EN VALIDACION' in e.upper() or 'PTEVALIDACION' in e.upper():
        return '⏳ En validación'
    
    if 'PTE ROLADO' in e.upper() or 'PENDIENTE ROLADO' in e.upper():
        return '⏳ Pendiente activación en el sistema'
    
    if 'PENDIENTE' in e.upper() and 'FIRMA' in e.upper():
        return '⏳ Pendiente de firma'
    
    if 'PENDIENTE COTIZACIÓN' in e.upper() and 'ACTA' in e.upper():
        return '⏳ Faltan: cotización y acta'
    
    if 'SUPERVISOR DEL CONTRATO INDICA QUE NO CONTINUAN' in e.upper():
        return '❌ Tu supervisor indicó que no continúan contigo'
    
    if 'SUPERVISORA INFORMA DE LA NO CONTINUIDAD' in e.upper():
        return '❌ Tu supervisora informó que no continúas'
    
    if 'PROCESO FINALIZADO' in e.upper() or 'CONTRATISTA ES CAMBIADO' in e.upper():
        return '✅ Proceso finalizado (fuiste cambiado por otro experto)'
    
    if 'PROCESO FINALIZADO' in e.upper():
        return '✅ Proceso finalizado'
    
    if 'SE REMITE AL AREA DE JURIDICA' in e.upper() or 'SE REMITE AL ÁREA DE JURÍDICA' in e.upper():
        return '⏳ Se envió al área jurídica para revisión'
    
    if 'SE REALIZA AJUSTE' in e.upper():
        return '🔧 Se realizó un ajuste al contrato'
    
    if 'SUPERVISOR DEL CONTRATO' in e.upper() and 'CAMBIA EL EXPERTO' in e.upper():
        return '🔄 Tu supervisor cambió de experto'
    
    if 'CAMBIAR CONTRATISTA' in e.upper() or 'CAMBIA EL EXPERTO' in e.upper() or 'CAMBIO DE EXPERTO' in e.upper():
        return '🔄 Se cambió de experto'
    
    if 'SE LE SOLICITA' in e.upper():
        return '📧 Te solicitaron algo'
    
    if 'SE CARGA ACTA' in e.upper() or 'SE  CARGA ACTA' in e.upper():
        return '✅ El acta de inicio ya está cargada'
    
    if 'SE CARGA SOLICITUD' in e.upper() or 'SE CREA SOLICITUD' in e.upper():
        return '✅ Tu solicitud fue creada'
    
    if 'SE REMITE A FIRMA' in e.upper():
        return '📝 Para firma'
    
    if 'SE APRUEBA' in e.upper() or 'APROBADO' in e.upper():
        return '✅ Aprobado'
    
    if 'SE RECHAZA' in e.upper() or 'RECHAZADO' in e.upper():
        return '❌ Rechazado'
    
    if 'SE DESISTE' in e.upper() or 'DESISTE' in e.upper():
        return '❌ Desistió'
    
    if 'FUERA DEL PAIS' in e.upper() or 'FUERA DEL PAÍS' in e.upper():
        return '❌ El experto está fuera del país y no puede continuar'
    
    if 'SE CARGA' in e.upper():
        return '✅ Cargado en el sistema'
    
    if 'ESTA CREADO' in e.upper() or 'ESTA CREADA' in e.upper():
        return '✅ Tu cuenta está creada en el sistema'
    
    if 'CONTRATISTA' in e.upper() and 'DESISTE' in e.upper():
        return '❌ El contratista desistió'
    
    if 'PENDIENTE' in e.upper() and 'FIRMA' in e.upper():
        return '⏳ Pendiente de firma'
    
    # Si empieza con fecha, mostrar fecha formateada
    if e[0].isdigit():
        fecha_formateada = formatear_fecha(e)
        return f"📅 {fecha_formateada}"
    
    # Si no matcheó nada
    return None


def traducir_observacion(texto_observacion):
    """Convierte observaciones técnicas a lenguaje humano"""
    if not texto_observacion:
        return None
    
    texto = str(texto_observacion).strip()
    
    if len(texto) < 3:
        return None
    
    if texto.lower() in ['nan', 'none', 'null']:
        return None
    
    texto = limpiar_texto(texto)
    
    if not texto or texto == 'nan':
        return None
    
    lineas = texto.split('\n')
    lineas_traducidas = []
    
    for linea in lineas:
        linea = linea.strip()
        if not linea:
            continue
        
        linea_traducida = traducir_linea(linea)
        if linea_traducida:
            # Agregar la fecha al inicio si la línea tiene una
            fecha = extraer_fecha(linea)
            if fecha:
                linea_traducida = f"📅 **{fecha}**: {linea_traducida}"
            lineas_traducidas.append(linea_traducida)
    
    if not lineas_traducidas:
        return None
    
    return "🔄 **HISTORIAL DE TU PROCESO:**\n\n" + "\n".join(lineas_traducidas[:10])


def limpiar_texto(texto):
    """Limpia el texto de caracteres raros"""
    import re
    texto = texto.replace('"', "'")
    texto = re.sub(r' +', ' ', texto)
    texto = re.sub(r'\n+', '\n', texto)
    return texto.strip()


def extraer_fecha(texto):
    """Extrae la primera fecha del texto y la formatea"""
    import re
    patron = r'\b(\d{1,2})[/\-](\d{1,2})[/\-](\d{2,4})\b'
    match = re.search(patron, texto)
    
    if match:
        dia, mes, anio = match.groups()
        if mes in MESES:
            return f"{dia} de {MESES[mes]} de {anio}"
    return None


def traducir_linea(linea):
    """Traduce UNA línea de observación"""
    l = linea.upper()
    
    # CASOS ESPECIALES
    if 'FIRMADO EN CARPETA' in l or 'CONTRATO FIRMADO' in l:
        return '✅ Tu contrato ya está firmado y archivado'
    
    if 'NO CONTINUA PROCESO' in l or 'NO CONTINÚA PROCESO' in l:
        if 'CONTRATISTA DESDE UNIMINUTO' in l:
            return '❌ El proceso no continúa (decisión de UNIMINUTO)'
        if 'Marzo 26' in l:
            return '❌ El proceso no continúa (decisión del programa)'
        if 'Mayo 05' in l:
            return '❌ El proceso no continúa (decisión del programa)'
        return '❌ El proceso no continúa'
    
    if 'EXPERTO DESISTE' in l or 'EXPERTODESISTE' in l:
        return '❌ El experto desistió del proceso'
    
    if 'CONTRATISTA DESISTE' in l:
        return '❌ El contratista desistió'
    
    if 'FUERA DEL PAIS' in l or 'FUERA DEL PAÍS' in l:
        return '❌ El experto está fuera del país, no puede continuar'
    
    if 'PROCESO FINALIZADO' in l or 'CONTRATISTA ES CAMBIADO' in l:
        return '✅ Proceso finalizado (fuiste cambiado por otro experto)'
    
    # COMUNICACIONES
    if 'SE ENVIA CORREO' in l or 'SE REMITE CORREO' in l:
        if 'CON COPIA AL SUPERVISOR' in l or 'CON COPIA LA SUPERVISOR' in l:
            return '📧 Te enviaron correo (con copia a tu supervisor)'
        if 'SOLICITANDO DOCUMENTOS' in l:
            return '📧 Te enviaron correo pidiendo documentos'
        if 'SOLICITANDO REGISTRO' in l:
            return '📧 Te enviaron correo para que te registres'
        if 'INFORMANDO' in l or 'CON INFORMACION' in l:
            return '📧 Te enviaron correo informando'
        if 'NOTIFICANDO' in l or 'NOTIFICA' in l:
            return '📧 Te enviaron correo notificando'
        if 'RATIFICANDO' in l:
            return '📧 Te recordaron por correo'
        if 'REITERANDO' in l:
            return '📧 Te enviaron correo reiterando'
        if 'MAL REALIZADO' in l:
            return '📧 Te enviaron correo sobre un error'
        if 'SUPERVISOR' in l:
            return '📧 Te enviaron correo (con copia a tu supervisor)'
        return '📧 Te enviaron correo'
    
    if 'SE LE LLAMA' in l or 'SE LE HACE LLAMADA' in l or 'SE LE HACE LLAMADO' in l:
        if 'NO CONTESTA' in l:
            return '📞 Te llamaron, no contestaste'
        if 'MENSAJE' in l:
            return '📞 Te llamaron y dejaron mensaje'
        return '📞 Te llamaron'
    
    if 'SE REALIZA LLAMADA' in l or 'SE HACE COMUNICACION' in l:
        if 'NO CONTESTA' in l:
            return '📞 Te llamaron, no contestaste'
        if 'MENSAJE DE VOZ' in l:
            return '📞 Te llamaron y dejaron mensaje de voz'
        if 'EN 3 OPORTUNIDADES' in l or 'EN REPETIDAS' in l:
            return '📞 Te llamaron varias veces, no respondiste'
        if 'EN 2 OPORTUNIDADES' in l:
            return '📞 Te llamaron 2 veces, no respondiste'
        if 'INDICA' in l or 'INFORMA' in l:
            return '📞 Te llamaron para informarte'
        if 'SOLICITA' in l:
            return '📞 Te llamaron para solicitarte algo'
        if 'VIA TELEFONICA' in l or 'VÍA TELEFÓNICA' in l:
            return '📞 Se comunicaron contigo por teléfono'
        return '📞 Se comunicaron contigo por teléfono'
    
    if 'SE REALIZA GESTION TELEFONICA' in l:
        return '📞 Intentaron llamarte'
    
    if 'SE REALIZA COMUNICACION' in l:
        if 'NO CONTESTA' in l:
            return '📞 No contestaste'
        if 'VIA TELEFONICA' in l or 'VÍA TELEFÓNICA' in l:
            return '📞 Se comunicaron contigo por teléfono'
        return '📞 Se comunicaron contigo'
    
    if 'SE LE INFORMA' in l or 'SE NOTIFICA' in l or 'SE LE NOTIFICA' in l:
        if 'SOBRE CORRECCION' in l or 'DEBE CORREGIR' in l:
            return '📧 Te notificaron que debes corregir algo'
        if 'REGISTRO MAL' in l or 'REGISTRO ERRADO' in l:
            return '📧 Te notificaron que tu registro está mal'
        if 'DOCUMENTOS CON CONTRASEÑA' in l:
            return '📧 Te notificaron que los documentos tienen contraseña'
        if 'RECHAZO' in l:
            return '📧 Te notificaron el rechazo'
        if 'CORRECCION DEL ARL' in l:
            return '📧 Te notificaron sobre corrección de ARL'
        if 'CORRECCION DEL RUT' in l or 'DEBE ACTUALIZAR EL RUT' in l:
            return '📧 Te notificaron que debes corregir el RUT'
        if 'DOCUMENTOS' in l:
            return '📧 Te notificaron sobre documentos'
        if 'NUEVAMENTE' in l:
            return '📧 Te notificaron nuevamente'
        if 'NOVEDADES' in l:
            return '📧 Te notificaron sobre novedades'
        return '📧 Te notificaron'
    
    if 'SE LE NOTIFICA A SUPERVISOR' in l or 'SE NOTIFICA A SUPERVISOR' in l or 'SE NOTIFICA AL SUPERVISOR' in l:
        return '📧 Se notificó a tu supervisor'
    
    if 'SE INTENTA HACER COMUNICACION' in l or 'SE INTENTA CONTACTAR' in l:
        return '📞 Intentaron contactarte sin éxito'
    
    if 'LINEA APAGADA' in l or 'BUZON DE VOZ' in l:
        return '📞 Tu teléfono estaba apagado/buzón'
    
    if 'WHATSAPP' in l:
        return '💬 Contacto por WhatsApp'
    
    # REGISTRO Y PORTAL
    if 'SE RECHAZA REGISTRO' in l or 'REGISTRO RECHAZADO' in l or 'SE RECHAZO EL REGISTRO' in l or 'SE RECHAZO' in l:
        if 'SEDE' in l:
            return '❌ Tu registro fue rechazado (te registraste en la sede equivocada)'
        if 'RUT' in l:
            return '❌ Tu registro fue rechazado (problema con tu RUT)'
        if 'DOCUMENTO' in l:
            return '❌ Tu registro fue rechazado (problema con documentos)'
        if 'REGIMEN' in l:
            return '❌ Tu registro fue rechazado (régimen incorrecto)'
        if 'CONTRASEÑA' in l or 'CLAVE' in l:
            return '❌ Tu registro fue rechazado (documentos con contraseña)'
        return '❌ Tu registro fue rechazado'
    
    if 'SE APRUEBA EN EL PORTAL' in l or 'SE APRUEBA PROVEEDOR' in l or 'APROBADO EN PORTAL' in l or 'REGISTRO APROBADO' in l or 'SE APRUEBA REGISTRO' in l:
        return '✅ Tu registro fue aprobado en el portal'
    
    if 'PTE VALIDACION' in l or 'EN VALIDACION' in l:
        if 'DOCUMENTOS' in l:
            return '⏳ Tus documentos están en validación'
        return '⏳ Tu registro está en validación'
    
    if 'PTE ROLADO' in l or 'PENDIENTE ROLADO' in l:
        return '⏳ Pendiente activación en el sistema'
    
    if 'SE REALIZA REGISTRO' in l or 'PROVEEDOR SE REGISTRA' in l or 'SE REGISTRA EN PORTAL' in l or 'SE REGISTRA' in l:
        if 'MANERA ERRADA' in l or 'MAL' in l or 'INCORRECTA' in l:
            return '⚠️ Te registraste pero mal. Debes corregirlo'
        if 'SEDE PRINCIPAL' in l or 'SEDE CUNDINAMARCA' in l:
            return '⚠️ Te registraste en la sede equivocada'
        return '✅ Te registraste en la plataforma'
    
    if 'NO SE HA REGISTRADO' in l or 'SIN REGISTRO' in l or 'AUN SIN REGISTRO' in l:
        return '⚠️ Aún no te has registrado en la plataforma'
    
    if 'SE SOLICITA REGISTRO' in l or 'SOLICITAR REGISTRO' in l:
        return '📧 Te pidieron registrarte en la plataforma'
    
    if 'SE SOLICITA CREACION' in l or 'SE SOLICITA  CREACION' in l:
        return '📧 Te pidieron crear tu cuenta en la plataforma'
    
    if 'SE SOLICITAN DOCUMENTOS' in l or 'SE SOLICITA DOCUMENTACION' in l or 'SOLICITANDO DOCUMENTOS' in l or 'SE SOLICITAN DOCUMENTOS ACTUALIZADOS' in l:
        return '📧 Te pidieron enviar documentos'
    
    if 'SE SOLICITA COTIZACION' in l or 'SE SOLICITA COTIZACIÓN' in l or 'PTE COTIZACION' in l or 'PENDIENTE COTIZACIÓN' in l:
        return '📧 Te pidieron la cotización firmada'
    
    if 'SE SOLICITA EXAMEN' in l or 'SE SOLICITA EXAMEN MEDICO' in l or 'PTE EXAMEN' in l or 'PENDIENTE EXAMEN' in l:
        return '📧 Te pidieron el examen médico'
    
    if 'SE LE HACE ACOMPAÑAMIENTO' in l or 'SE REALIZA ACOMPAÑAMIENTO' in l or 'ACOMPAÑAMIENTO POR TEAMS' in l:
        return '💻 Te acompañaron en el proceso'
    
    if 'NO CONTESTA' in l:
        if 'MENSAJE' in l:
            return '📞 No contestaste, dejaron mensaje'
        if 'BUZON' in l or 'APAGADA' in l:
            return '📞 Tu teléfono estaba apagado/buzón'
        return '📞 No contestaste'
    
    # DOCUMENTOS
    if 'CARGA DOCUMENTOS' in l or 'REMITE DOCUMENTOS' in l or 'ENVIA DOCUMENTOS' in l or 'SUBEN DOCUMENTOS' in l:
        return '✅ Enviaste los documentos'
    
    if 'CARGA ACTA' in l or 'SE CARGA ACTA' in l:
        return '✅ El acta de inicio ya está cargada'
    
    if 'CARGA SOLICITUD' in l or 'SE CREA SOLICITUD' in l or 'CREA SOLICITUD' in l or 'SE CREA SOLICITUD' in l:
        return '✅ Tu solicitud fue creada en el sistema'
    
    if 'CORRECCION DEL RUT' in l or 'ACTUALIZACION DEL RUT' in l or 'CORREGIR EL RUT' in l or 'DEBE ACTUALIZAR EL RUT' in l:
        return '📧 Te notificaron que debes actualizar/corregir tu RUT'
    
    if 'CORRECCION DEL ARL' in l:
        return '📧 Te notificaron sobre corrección de ARL'
    
    if 'DOCUMENTOS CON CONTRASEÑA' in l or 'DOCUMENTOS CON CLAVE' in l:
        return '⚠️ Tus documentos tienen contraseña, debes quitarla'
    
    # CONTRATOS Y FIRMAS
    if 'SE REMITE PARA FIRMA DEL EXPERTO' in l or 'CONTRATO PARA FIRMA DEL EXPERTO' in l:
        return '📝 Tu contrato está para tu firma'
    
    if 'SE REMITE PARA FIRMA DEL RECTOR' in l or 'CONTRATO PARA FIRMA DEL RECTOR' in l or 'CONTRATO PARA FIRMA DEL SEÑOR RECTOR' in l:
        return '📝 Tu contrato está para firma del rector'
    
    if 'SE REMITE PARA FIRMA' in l or 'CONTRATO PARA FIRMA' in l or 'EN FIRMA DE CONTRATISTA' in l:
        return '📝 Tu contrato está para firma'
    
    if 'SE REMITE A FIRMA' in l or 'REMITE A FIRMA' in l:
        return '📝 Para firma'
    
    if 'CONTRATO FIRMADO' in l or 'CONTRATO EN FIRMA' in l or 'HA FIRMADO' in l or 'CONTRA FIRMADO' in l:
        return '✅ Tu contrato ya está firmado'
    
    if 'NO HA ENVIADO' in l or 'AUN NO HA ENVIADO' in l or 'AÚN NO HA ENVIADO' in l:
        if 'CONTRATO FIRMADO' in l:
            return '⚠️ Aún no has enviado el contrato firmado'
        if 'DOCUMENTOS' in l:
            return '⚠️ Aún no has enviado documentos'
        return '⚠️ Aún no has enviado lo solicitado'
    
    if 'SE REMITE' in l and 'JURIDICA' in l:
        return '⏳ Se envió al área jurídica'
    
    # PENDIENTES
    if 'PTE ACTA' in l or 'PENDIENTE ACTA' in l:
        return '⏳ Falta cargar el acta de inicio'
    
    if 'PTE COTIZACION' in l or 'PENDIENTE COTIZACION' in l:
        return '⏳ Falta la cotización firmada'
    
    if 'PTE JURIDICA' in l or 'PENDIENTE JURIDICA' in l or 'PDT JURIDICA' in l or 'PDT AREA JURIDICA' in l:
        return '⏳ En revisión por el área jurídica'
    
    if 'PTE EXAMEN' in l or 'PENDIENTE EXAMEN' in l:
        return '⏳ Falta el examen médico'
    
    if 'PTE DOCUMENTOS' in l or 'PENDIENTE DOCUMENTOS' in l or 'SIN DOCUMENTOS' in l:
        return '⏳ Faltan documentos por enviar'
    
    if 'PTE FIRMA' in l or 'PENDIENTE FIRMA' in l:
        return '⏳ Pendiente de firma'
    
    if 'PTE APROBACION' in l:
        return '⏳ Pendiente de aprobación'
    
    if 'PTE CTA DE COBRO' in l or 'PTE CUENTA DE COBRO' in l:
        return '⏳ Pendiente la cuenta de cobro'
    
    if 'PTE ROLADO' in l:
        return '⏳ Pendiente activación en el sistema'
    
    if 'PTE AVAL' in l:
        return '⏳ Pendiente aprobación (aval)'
    
    if 'SE REMITE PARA FIRMA' in l:
        return '📝 Para firma'
    
    if 'SUPERVISOR' in l and 'CAMBIA' in l:
        return '🔄 Tu supervisor cambió de experto'
    
    if 'CAMBIA EL EXPERTO' in l or 'CAMBIO DE EXPERTO' in l or 'CAMBIO DE EXPERTRO' in l:
        return '🔄 Se cambió de experto'
    
    if 'PROCESO FINALIZADO' in l or 'CONTRATISTA ES CAMBIADO' in l:
        return '✅ Proceso finalizado (fuiste cambiado)'
    
    if 'SOLPEDIDO ELIMINADO' in l:
        return '❌ Este contrato fue eliminado. No se generarán pagos.'
    if 'RENOVACIÓN LICENCIA' in l:
        return '🔄 Renovación de licencia solicitada.'
    
    # Si no matcheó ningún patrón, devolver la línea limpia con fecha
    fecha = extraer_fecha(linea)
    if fecha:
        return f"📝 {linea[:100]}"
    return f"📝 {linea[:100]}"


def limpiar_y_traducir(texto):
    return traducir_observacion(texto)
