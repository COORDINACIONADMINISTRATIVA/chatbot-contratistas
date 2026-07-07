"""
Intérprete de observaciones y estados de contratistas
"""

# Diccionario de estados
ESTADOS_TRADUCIDOS = {
    'FIRMADO EN CARPETA': '✅ Tu contrato ya está firmado y archivado',
    'CONTRATO FIRMADO EN CARPETA': '✅ Tu contrato ya está firmado y archivado',
    'CONTRATO FIRMADO POR LAS PARTES': '✅ Tu contrato ya está firmado por las partes',
    'EN PROCESO': '⏳ Tu proceso está en revisión',
    'PENDIENTE': '⏳ Hay algo pendiente por hacer',
    'APROBADO': '✅ Tu proceso fue aprobado',
    'RECHAZADO': '❌ Tu proceso fue rechazado',
    'EN FIRMA': '📝 Tu contrato está en proceso de firma',
    'PENDIENTE ACTA': '⏳ Falta cargar el acta de inicio',
    'PENDIENTE COTIZACION': '⏳ Falta la cotización firmada',
    'PENDIENTE JURIDICA': '⏳ Está en revisión por el área jurídica',
    'PENDIENTE EXAMEN': '⏳ Falta el examen médico',
    'PENDIENTE DOCUMENTOS': '⏳ Faltan documentos por enviar',
    'NO REGISTRA': '⚠️ Aún no te has registrado en la plataforma',
    'NO CONTINUA': '❌ El proceso no continúa',
    'EXPERTO DESISTE': '❌ El experto desistió',
}

# Frases en observaciones
FRASES = {
    'se envia correo': '📧 Te enviaron correo',
    'se remite correo': '📧 Te enviaron correo',
    'se solicita': '📧 Te pidieron',
    'se solicita registro': '📧 Te pidieron registrarte',
    'se solicita creacion': '📧 Te pidieron crear tu cuenta',
    'se solicita documento': '📧 Te pidieron documentos',
    'se solicita actualizacion': '📧 Te pidieron actualizar',
    'se rechaza': '❌ Tu registro fue rechazado',
    'se rechaza registro': '❌ Tu registro fue rechazado',
    'se aprueba': '✅ Aprobado',
    'se aprueba en el portal': '✅ Tu registro fue aprobado en el portal',
    'se aprueba registro': '✅ Tu registro fue aprobado',
    'no contesta': '📞 No contestaste',
    'no se logra': '📞 No se logró comunicación',
    'pte documento': '⏳ Pendiente documentos',
    'pte examen': '⏳ Pendiente examen médico',
    'pte acta': '⏳ Pendiente acta',
    'pte cotizacion': '⏳ Pendiente cotización',
    'pte firma': '⏳ Pendiente firma',
    'contraseña': '🔐 Tiene contraseña',
    'con clave': '🔐 Con clave',
    'sede incorrecta': '❌ Sede mal seleccionada',
    'se registra': '✅ Te registraste',
    'sede principal': '❌ Sede equivocada',
    'sede cundinamarca': '❌ Sede equivocada',
    'se realiza': '✅ Se realizó',
    'rechazad': '❌ Rechazado',
    'aprobad': '✅ Aprobado',
    'no se logra': '📞 No se logró comunicación',
    'reagendar': '📅 Reagendar',
    'no responde': '📞 No responde',
    'cumpleaños': '🎂',
    'se carga': '✅ Se cargó',
    'se aprueba': '✅ Se aprobó',
    'no registra': '⚠️ No registra',
    'rechazo': '❌ Rechazo',
    'se le notifica': '📧 Se le notificó',
    'se valida': '✅ Se validó',
    'se valido': '✅ Se validó',
    'firmado en carpeta': '✅ Contrato firmado en carpeta',
    'aprobado en portal': '✅ Aprobado en portal',
    'rechazado en portal': '❌ Rechazado en portal',
    'novedad': '⚠️ Novedad',
    'problema': '❌ Problema',
    'sede': '📍 Sede',
    'extranjero': '🌎 Extranjero',
    'documentos con clave': '🔐 Documentos con clave',
    'se reenvia': '📧 Se reenvió',
    'se ratifica': '📧 Se ratifica',
    'se indica': '📧 Se indica',
    'rechazad': '❌',
    'rechaz': '❌',
    'aprobad': '✅',
    'se informa': '📧 Se informa',
    'pendiente': '⏳ Pendiente',
    'documento': '📄 Documento',
}


def traducir_estado(estado):
    """Traduce el estado a lenguaje humano"""
    if not estado:
        return None
    
    e = str(estado).strip()
    
    if e.lower() in ['nan', 'none', 'null', '']:
        return None
    
    # Buscar coincidencia exacta
    if e in ESTADOS_TRADUCIDOS:
        return ESTADOS_TRADUCIDOS[e]
    
    # Buscar coincidencia parcial
    for key, value in ESTADOS_TRADUCIDOS.items():
        if key in e.upper() or e.upper() in key:
            return value
    
    return None


def traducir_observacion(texto_observacion):
    """Traduce la observación a lenguaje humano"""
    if not texto_observacion:
        return None
    
    texto = str(texto_observacion).strip()
    
    if texto.lower() in ['nan', 'none', 'null', '']:
        return None
    
    if len(texto) < 5:
        return None
    
    lineas = texto.split('\n')
    lineas_traducidas = []
    
    for linea in lineas:
        linea = linea.strip()
        if not linea:
            continue
        
        # Extraer fecha si existe
        fecha = extraer_fecha(linea)
        traduccion = traducir_linea(linea)
        
        if traduccion:
            if fecha:
                lineas_traducidas.append(f"📅 **{fecha}**: {traduccion}")
            else:
                lineas_traducidas.append(traduccion)
    
    if not lineas_traducidas:
        return None
    
    return "🔄 **HISTORIAL DE TU PROCESO:**\n\n" + "\n".join(lineas_traducidas[:10])


def extraer_fecha(texto):
    """Extrae la primera fecha del texto"""
    import re
    
    # Formato DD/MM/YYYY
    match = re.search(r'(\d{1,2})/(\d{1,2})/(\d{2,4})', texto)
    if match:
        dia, mes, anio = match.groups()
        if len(anio) == 2:
            anio = '20' + anio
        meses = {
            '01': 'enero', '02': 'febrero', '03': 'marzo', '04': 'abril',
            '05': 'mayo', '06': 'junio', '07': 'julio', '08': 'agosto',
            '09': 'septiembre', '10': 'octubre', '11': 'noviembre', '12': 'diciembre'
        }
        if mes in meses:
            return f"{dia} de {meses[mes]} de {anio}"
    
    # Formato YYYYMMDD
    match = re.search(r'(20\d{2})(\d{2})(\d{2})', texto)
    if match:
        anio, mes, dia = match.groups()
        meses = {
            '01': 'enero', '02': 'febrero', '03': 'marzo', '04': 'abril',
            '05': 'mayo', '06': 'junio', '07': 'julio', '08': 'agosto',
            '09': 'septiembre', '10': 'octubre', '11': 'noviembre', '12': 'diciembre'
        }
        if mes in meses:
            return f"{dia} de {meses[mes]} de {anio}"
    
    return None


def traducir_linea(linea):
    """Traduce una línea individual"""
    l = linea.upper()
    
    # Casos específicos primero
    if 'FIRMADO EN CARPETA' in l or 'CONTRATO FIRMADO' in l:
        return '✅ Tu contrato ya está firmado y archivado'
    
    if 'EN TRÁMITE' in l or 'EN TRAMITE' in l:
        return '⏳ Está en proceso de validación'
    
    if 'SE RECHAZA' in l or 'RECHAZADO' in l or 'RECHAZAD' in l:
        if 'SEDE' in l:
            return '❌ Tu registro fue rechazado (sede incorrecta)'
        if 'RUT' in l:
            return '❌ Tu registro fue rechazado (problema con el RUT)'
        if 'DOCUMENTO' in l:
            return '❌ Tu registro fue rechazado (problemas con documentos)'
        return '❌ Tu registro fue rechazado'
    
    if 'SE APRUEBA' in l or 'APROBAD' in l:
        if 'PORTAL' in l:
            return '✅ Tu registro fue aprobado en el portal'
        return '✅ Tu registro fue aprobado'
    
    if 'NO CONTESTA' in l or 'NO RESPONDE' in l:
        return '📞 Te llamaron pero no contestaste'
    
    if 'SE LLAMA' in l or 'SE LE LLAMA' in l or 'HACER COMUNICACION' in l:
        return '📞 Te llamaron'
    
    if 'DEJA MENSAJE' in l or 'SE DEJA MENSAJE' in l or 'MENSAJE DE VOZ' in l:
        return '🎤 Te dejaron un mensaje de voz'
    
    if 'CORREO' in l and 'ENVI' in l:
        return '📧 Te enviaron correo'
    
    if 'SOLICITA' in l and 'DOCUMENTO' in l:
        return '📧 Te pidieron documentos'
    
    if 'SOLICITA' in l and 'REGISTRO' in l:
        return '📧 Te pidieron registrarte'
    
    if 'SOLICITA' in l and 'CREACION' in l:
        return '📧 Te pidieron crear tu cuenta'
    
    if 'PTE' in l or 'PENDIENTE' in l:
        if 'ACTA' in l:
            return '⏳ Falta cargar el acta'
        if 'EXAMEN' in l:
            return '⏳ Falta el examen médico'
        if 'COTIZACION' in l or 'COTIZACIÓN' in l:
            return '⏳ Falta la cotización'
        if 'FIRMA' in l:
            return '⏳ Pendiente de firma'
        if 'DOCUMENTO' in l:
            return '⏳ Faltan documentos'
        if 'ROLADO' in l:
            return '⏳ Pendiente activación en el sistema'
        return '⏳ Pendiente'
    
    if 'CONTRASEÑA' in l or 'CON CLAVE' in l:
        return '🔐 Tus documentos tienen contraseña'
    
    if 'SEDE' in l and ('PRINCIPAL' in l or 'CUNDINAMARCA' in l):
        return '❌ Te registraste en la sede equivocada'
    
    if 'EXTRANJERO' in l or 'POR CONECTA' in l:
        return '🌎 Necesitas registro por Conecta (extranjeros)'
    
    if 'NOVEDAD' in l:
        return '⚠️ Hay una novedad'
    
    if 'CARG' in l and 'SOLICITUD' in l:
        return '✅ Se cargó la solicitud'
    
    if 'CARG' in l and 'ACTA' in l:
        return '✅ Se cargó el acta'
    
    # Si no se encontró nada
    return None
