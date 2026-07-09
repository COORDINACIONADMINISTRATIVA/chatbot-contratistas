import re
import json
from datetime import datetime

from contratacion.lector_pdf import leer_pdf


# ---------------------------------------------------------------------------
# Catálogos de referencia
# ---------------------------------------------------------------------------

TIPOS_DOCUMENTO = [
    "Cédula de Ciudadanía",
    "Cédula de Extranjería",
    "NIT",
    "Pasaporte",
    "Registro Civil",
    "Tarjeta de Identidad",
    "Carné Diplomático",
]

ACTIVIDADES_EDUCACION = [
    '8560', '8550', '8551', '8552', '8559',
    '8541', '8542', '8543', '8544', '8549',
    '8521', '8522', '8523', '8530', '8520'
]

PALABRAS_NO_NOMBRE = {
    "COLOMBIA", "IDENTIFICACIÓN", "IDENTIFICACION", "UBICACIÓN", "UBICACION",
    "CLASIFICACIÓN", "CLASIFICACION", "CONTRIBUYENTE", "IMPORTANTE",
    "RESPONSABILIDADES", "CALIDADES", "ATRIBUTOS", "EXPORTADORES",
    "SOCIOS", "MIEMBROS", "JUNTAS", "CONSORCIOS", "TEMPORALES",
    "DIAN", "FORMULARIO", "REGISTRO", "ÚNICO", "TRIBUTARIO",
}


# ---------------------------------------------------------------------------
# Extracción de campos individuales
# ---------------------------------------------------------------------------

def _extraer_tipo_documento(texto):
    for tipo in TIPOS_DOCUMENTO:
        if tipo.lower() in texto.lower():
            return tipo
    return None


def _extraer_cedula(texto, tipo_documento):
    """
    Extrae la cédula/NIT de 6-10 dígitos.
    Evita capturar el código del tipo de documento (ej: "13" de Cédula).
    """
    # Método 1: Buscar justo después del tipo de documento
    if tipo_documento:
        # Buscar patrón: "Cédula de Ciudadanía" seguido de dígitos con espacios
        patron = re.escape(tipo_documento) + r'\s+([\d\s]+)'
        m = re.search(patron, texto, re.IGNORECASE)
        if m:
            digitos = re.sub(r'\D', '', m.group(1))
            # Filtrar para obtener solo la cédula (6-10 dígitos)
            # Si hay más de 10 dígitos, buscar la cédula real
            if len(digitos) > 10:
                # Buscar cualquier grupo de 6-10 dígitos dentro
                cedula_match = re.search(r'\d{6,10}', digitos)
                if cedula_match:
                    return cedula_match.group()
            elif 6 <= len(digitos) <= 10:
                return digitos

    # Método 2: Buscar "Número de Identificación" seguido de dígitos
    m = re.search(r'Número\s+de\s+Identificaci[oó]n\s*[:\n]?\s*([\d\s]+)', texto, re.IGNORECASE)
    if m:
        digitos = re.sub(r'\D', '', m.group(1))
        if 6 <= len(digitos) <= 10:
            return digitos
        if len(digitos) > 10:
            cedula_match = re.search(r'\d{6,10}', digitos)
            if cedula_match:
                return cedula_match.group()

    # Método 3: Buscar "NIT" seguido de dígitos
    m = re.search(r'NIT\s*[:\n]?\s*([\d\s]+)', texto, re.IGNORECASE)
    if m:
        digitos = re.sub(r'\D', '', m.group(1))
        if 6 <= len(digitos) <= 10:
            return digitos

    # Método 4: Buscar en el formato "26. Número de Identificación"
    m = re.search(r'26\.\s*Número\s+de\s+Identificaci[oó]n\s*([\d\s]+)', texto, re.IGNORECASE)
    if m:
        digitos = re.sub(r'\D', '', m.group(1))
        if 6 <= len(digitos) <= 10:
            return digitos

    # Método 5: Fallback - buscar cualquier número de 6-10 dígitos
    # que NO esté precedido por "1 3" (código de cédula)
    m = re.search(r'(?<![1]\s[3]\s)(?:\d\s+){5,9}\d', texto)
    if m:
        return re.sub(r'\D', '', m.group())

    # Fallback final: cualquier número de 6-10 dígitos
    m = re.search(r'\b\d{6,10}\b', texto)
    if m:
        return m.group()

    return None


def _extraer_tipo_contribuyente(texto):
    if re.search(r'persona\s+natural', texto, re.IGNORECASE):
        return "Persona natural o sucesión ilíquida"
    if re.search(r'persona\s+jur[ií]dica', texto, re.IGNORECASE):
        return "Persona jurídica"
    return None


def _lineas_utiles(texto):
    return [l.strip() for l in texto.split('\n')]


def _extraer_nombre_o_razon_social(texto, tipo_contribuyente):
    """
    Busca el nombre completo (persona natural) o razón social (persona jurídica).
    """
    # Para persona jurídica, buscar específicamente "Razón social"
    if tipo_contribuyente and 'jurídica' in tipo_contribuyente.lower():
        # Buscar "35. Razón social" o "Razón social" seguido del nombre
        for linea in _lineas_utiles(texto):
            if '35.' in linea and 'RAZON SOCIAL' in linea.upper():
                # Extraer lo que está después del número
                partes = re.split(r'35\.\s*Raz[oó]n\s+social\s*[:\n]?', linea, flags=re.IGNORECASE)
                if len(partes) > 1:
                    nombre = partes[1].strip()
                    if nombre and len(nombre) > 3 and not nombre[0].isdigit():
                        return nombre, {'razon_social': nombre}

            if 'RAZON SOCIAL' in linea.upper() or 'RAZÓN SOCIAL' in linea.upper():
                # Buscar el nombre después de "Razón social"
                partes = re.split(r'Raz[oó]n\s+social\s*[:\n]?', linea, flags=re.IGNORECASE)
                if len(partes) > 1:
                    nombre = partes[1].strip()
                    if nombre and len(nombre) > 3 and not nombre[0].isdigit():
                        return nombre, {'razon_social': nombre}

    # Para persona natural o fallback general: buscar líneas en mayúsculas sostenidas
    candidatos = {}
    for linea in _lineas_utiles(texto):
        if not linea or any(ch.isdigit() for ch in linea):
            continue
        palabras = linea.split()
        if not (2 <= len(palabras) <= 6):
            continue
        # Verificar que todas las palabras estén en mayúsculas con acentos
        if not all(re.fullmatch(r'[A-ZÁÉÍÓÚÑ]+', p) for p in palabras):
            continue
        primera = palabras[0]
        if primera in PALABRAS_NO_NOMBRE:
            continue
        candidatos[linea] = candidatos.get(linea, 0) + 1

    if not candidatos:
        # Si no hay candidatos y es persona jurídica, buscar cualquier línea larga en mayúsculas
        if tipo_contribuyente and 'jurídica' in tipo_contribuyente.lower():
            for linea in _lineas_utiles(texto):
                if len(linea) > 10 and linea.isupper() and not any(ch.isdigit() for ch in linea):
                    if not any(p in linea.upper() for p in ['COLOMBIA', 'IDENTIFICACIÓN', 'UBICACIÓN', 'DIAN']):
                        return linea, {'razon_social': linea}
        return None, {}

    # El nombre real suele repetirse (aparece también en la firma)
    nombre = max(candidatos.items(), key=lambda kv: (kv[1], len(kv[0])))[0]

    partes = {}
    if tipo_contribuyente and 'natural' in tipo_contribuyente.lower():
        palabras = nombre.split()
        if len(palabras) == 2:
            partes = {'primer_apellido': palabras[0], 'segundo_apellido': None,
                      'primer_nombre': palabras[1], 'otros_nombres': None}
        elif len(palabras) == 3:
            partes = {'primer_apellido': palabras[0], 'segundo_apellido': palabras[1],
                      'primer_nombre': palabras[2], 'otros_nombres': None}
        elif len(palabras) >= 4:
            partes = {'primer_apellido': palabras[0], 'segundo_apellido': palabras[1],
                      'primer_nombre': palabras[2], 'otros_nombres': ' '.join(palabras[3:])}
    else:
        partes = {'razon_social': nombre}

    return nombre, partes


def _extraer_correo(texto):
    m = re.search(r'[\w.\-]+@[\w.\-]+\.\w+', texto)
    return m.group() if m else None


def _extraer_direccion_y_telefonos(texto):
    """
    La dirección queda SIEMPRE una línea antes del correo, y los teléfonos
    (uno o dos números de 10 dígitos pegados) una línea después.
    """
    lineas = _lineas_utiles(texto)
    direccion = None
    telefonos = []

    idx_correo = None
    for i, linea in enumerate(lineas):
        if '@' in linea:
            idx_correo = i
            break

    if idx_correo is not None:
        # Dirección: línea previa no vacía, que no sea el bloque país/ciudad
        for j in range(idx_correo - 1, -1, -1):
            candidata = lineas[j].strip()
            if not candidata:
                continue
            if re.match(r'^COLOMBIA\b', candidata, re.IGNORECASE):
                break
            # Si la línea parece una dirección (tiene números y letras)
            if re.search(r'\d', candidata) and len(candidata) > 5:
                direccion = candidata
                break
            # Si no tiene números pero es larga, puede ser dirección
            if len(candidata) > 10 and not candidata.isupper():
                direccion = candidata
                break

        # Teléfonos: siguiente línea con dígitos
        for j in range(idx_correo + 1, min(idx_correo + 4, len(lineas))):
            digitos = re.sub(r'\D', '', lineas[j])
            if len(digitos) >= 7:
                if len(digitos) >= 20:
                    telefonos = [digitos[0:10], digitos[10:20]]
                elif len(digitos) > 10:
                    telefonos = [digitos[0:10], digitos[10:]]
                else:
                    telefonos = [digitos]
                break

    return direccion, telefonos


def _extraer_actividades_economicas(texto):
    """
    Busca tiras largas de dígitos sueltos y las interpreta como
    [código 4 dígitos][fecha AAAAMMDD 8 dígitos] pegados.
    """
    actividades = []
    for match in re.finditer(r'(?:\d[\s]*){12,60}', texto):
        bloque = re.sub(r'\D', '', match.group())
        i = 0
        while i + 12 <= len(bloque):
            codigo = bloque[i:i + 4]
            resto = bloque[i + 4:i + 12]
            if resto[:2] in ('19', '20'):
                anio, mes, dia = resto[:4], resto[4:6], resto[6:8]
                if 1 <= int(mes) <= 12 and 1 <= int(dia) <= 31 and 1990 <= int(anio) <= 2035:
                    actividades.append({
                        'codigo': codigo,
                        'fecha_inicio': f"{dia}/{mes}/{anio}"
                    })
                    i += 12
                    continue
            i += 1
    return actividades


def _extraer_responsabilidades(texto):
    """Estas SÍ vienen como texto plano tipo 'NN - Descripción' en el PDF."""
    encontradas = []
    for m in re.finditer(r'\b(\d{2})\s*-\s*([A-ZÁÉÍÓÚÑa-záéíóúñ][^\n\d]{3,80})', texto):
        codigo, descripcion = m.group(1), m.group(2).strip()
        item = f"{codigo} - {descripcion}"
        if item not in encontradas:
            encontradas.append(item)
    return encontradas


def _extraer_fecha_generacion_pdf(texto):
    """
    Busca la fecha de generación del PDF en el formato:
    "Fecha generación documento PDF: DD-MM-YYYY HH:MM:SSAM/PM"
    """
    # Primero intentar con el formato exacto
    m = re.search(
        r'Fecha\s*generaci[oó]n\s*documento\s*PDF:?\s*(\d{1,2})-(\d{1,2})-(\d{4})\s*(\d{1,2}:\d{2}:\d{2}\s*[AP]M)?',
        texto, re.IGNORECASE
    )
    if m:
        d, mo, y, hora = m.groups()
        try:
            fecha = datetime(int(y), int(mo), int(d))
            return {'fecha': fecha.strftime('%d/%m/%Y'), 'hora': hora, '_dt': fecha}
        except ValueError:
            pass

    # Buscar solo la fecha sin hora
    m = re.search(r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})\s*(?:$|\s)', texto)
    if m:
        d, mo, y = m.groups()
        try:
            fecha = datetime(int(y), int(mo), int(d))
            return {'fecha': fecha.strftime('%d/%m/%Y'), 'hora': None, '_dt': fecha}
        except ValueError:
            pass

    return None


def _extraer_fecha_actualizacion(texto):
    """
    Busca la fecha de actualización del RUT (formato: AAAA-MM-DD / HH:MM:SSPM).
    """
    m = re.search(r'(\d{4})-(\d{2})-(\d{2})\s*/\s*(\d{1,2}:\d{2}:\d{2}\s*[AP]M)', texto)
    if not m:
        return None
    y, mo, d, hora = m.groups()
    try:
        fecha = datetime(int(y), int(mo), int(d))
        return {'fecha': fecha.strftime('%d/%m/%Y'), 'hora': hora, '_dt': fecha}
    except ValueError:
        return None


def _extraer_marca_agua(texto):
    """
    Detecta la marca de agua del RUT buscando palabras clave en el texto.
    """
    t = texto.lower()

    # Buscar al inicio del documento (primeras líneas)
    primeras_lineas = '\n'.join(t.split('\n')[:30])

    # Buscar "Concepto" que indica el tipo de actualización
    concepto_match = re.search(r'concepto\s*(\d+)\s*(actualización|actualizacion|copia|certificado|en\s*tr[áa]mite)', t, re.IGNORECASE)
    if concepto_match:
        tipo = concepto_match.group(2).lower()
        if 'en trámite' in tipo or 'en tramite' in tipo:
            return 'en_tramite', "EN TRÁMITE (no sirve todavía)"
        if 'actualización' in tipo or 'actualizacion' in tipo:
            return 'valido', "Actualización"
        if 'copia' in tipo:
            return 'valido', "Copia"
        if 'certificado' in tipo:
            return 'valido', "Certificado"

    if 'en trámite' in t or 'en tramite' in t:
        return 'en_tramite', "EN TRÁMITE (no sirve todavía)"
    if 'actualización de oficio' in t or 'actualizacion de oficio' in t:
        return 'valido', "Actualización de oficio"
    if 'actualización' in t or 'actualizacion' in t:
        return 'valido', "Actualización"
    if 'copia' in t:
        return 'valido', "Copia"
    if 'certificado' in t:
        return 'valido', "Certificado"

    return 'desconocido', "No se pudo determinar la marca de agua del documento"


# ---------------------------------------------------------------------------
# API pública: JSON con todos los campos
# ---------------------------------------------------------------------------

def extraer_datos_rut(texto):
    """Devuelve un dict (JSON-serializable) con todos los campos del RUT."""
    tipo_documento = _extraer_tipo_documento(texto)
    tipo_contribuyente = _extraer_tipo_contribuyente(texto)
    cedula = _extraer_cedula(texto, tipo_documento)
    nombre_completo, partes_nombre = _extraer_nombre_o_razon_social(texto, tipo_contribuyente)
    correo = _extraer_correo(texto)
    direccion, telefonos = _extraer_direccion_y_telefonos(texto)
    actividades = _extraer_actividades_economicas(texto)
    responsabilidades = _extraer_responsabilidades(texto)
    fecha_generacion = _extraer_fecha_generacion_pdf(texto)
    fecha_actualizacion = _extraer_fecha_actualizacion(texto)
    marca_agua_estado, marca_agua_detalle = _extraer_marca_agua(texto)

    datos = {
        'tipo_documento': tipo_documento,
        'numero_identificacion': cedula,
        'tipo_contribuyente': tipo_contribuyente,
        'nombre_completo': nombre_completo,
        'nombre_desglosado': partes_nombre or None,
        'direccion': direccion,
        'correo': correo,
        'telefonos': telefonos,
        'actividades_economicas': actividades,
        'responsabilidades_calidades_atributos': responsabilidades,
        'fecha_generacion_pdf': fecha_generacion['fecha'] if fecha_generacion else None,
        'hora_generacion_pdf': fecha_generacion['hora'] if fecha_generacion else None,
        'fecha_actualizacion_rut': fecha_actualizacion['fecha'] if fecha_actualizacion else None,
        'marca_agua': marca_agua_estado,
        'marca_agua_detalle': marca_agua_detalle,
    }
    # metadatos internos usados por el validador (no se muestran al usuario)
    datos['_fecha_referencia_dt'] = (
        fecha_generacion['_dt'] if fecha_generacion else
        (fecha_actualizacion['_dt'] if fecha_actualizacion else None)
    )
    return datos


# ---------------------------------------------------------------------------
# Validación de reglas de negocio
# ---------------------------------------------------------------------------

class ValidadorRUT:
    def __init__(self):
        self.actividades_validas = ACTIVIDADES_EDUCACION

    def extraer_texto_pdf(self, ruta_pdf):
        return leer_pdf(ruta_pdf)

    def analizar_rut(self, ruta_pdf, contratista_info=None, cedula_esperada=None):
        resultados = {
            'valido': False, 'errores': [], 'advertencias': [],
            'exitos': [], 'datos_extraidos': {}
        }

        texto = self.extraer_texto_pdf(ruta_pdf)
        if not texto:
            resultados['errores'].append("No se pudo leer el PDF (¿es una imagen escaneada sin OCR disponible?)")
            return resultados

        datos = extraer_datos_rut(texto)
        
        # FILTRAR: Eliminar marca_agua y marca_agua_detalle de los datos mostrados
        datos_publicos = {k: v for k, v in datos.items() if not k.startswith('_') and k not in ['marca_agua', 'marca_agua_detalle']}
        resultados['datos_extraidos'] = datos_publicos

        # --- Marca de agua (solo para validación, no se muestra) ---
        if datos['marca_agua'] == 'en_tramite':
            resultados['errores'].append(f"❌ {datos['marca_agua_detalle']}")
        elif datos['marca_agua'] == 'valido':
            resultados['exitos'].append(f"✅ Marca de agua: {datos['marca_agua_detalle']} (válido)")
        else:
            resultados['advertencias'].append(f"⚠️ {datos['marca_agua_detalle']}")

        # --- Actividad económica ---
        codigos = [a['codigo'] for a in datos['actividades_economicas']]
        educacion = [c for c in codigos if c in self.actividades_validas]
        if educacion:
            if '8560' in educacion:
                resultados['exitos'].append("✅ Tiene la actividad 8560 (ideal)")
            else:
                resultados['exitos'].append(f"✅ Actividad de educación: {', '.join(sorted(set(educacion)))}")
        else:
            resultados['errores'].append(
                f"❌ No se encontró actividad de educación. Códigos detectados: {', '.join(codigos) if codigos else 'ninguno'}"
            )

        # --- Vigencia: usa SOLO la fecha de GENERACIÓN del PDF ---
        fecha_dt = None
        if datos.get('_fecha_referencia_dt'):
            fecha_dt = datos['_fecha_referencia_dt']

        if fecha_dt:
            dias = (datetime.now() - fecha_dt).days
            if dias <= 30:
                resultados['exitos'].append(f"✅ RUT generado hace {dias} días (vigente)")
            elif dias <= 365:
                # ERROR si es mayor a 30 días
                resultados['errores'].append(f"❌ El RUT tiene {dias} días (debe ser menor a 30 días de generación)")
            else:
                resultados['errores'].append(f"❌ El RUT es muy antiguo ({dias} días)")
        else:
            resultados['advertencias'].append("⚠️ No se pudo leer la fecha de generación del documento")

        # --- Cédula: se VERIFICA contra la que ya conocemos ---
        cedula_check = cedula_esperada or (contratista_info.get('cedula') if contratista_info else None)
        if cedula_check:
            digitos_esperados = re.sub(r'\D', '', str(cedula_check))
            if datos['numero_identificacion'] == digitos_esperados:
                resultados['exitos'].append(f"✅ La cédula del RUT coincide: {digitos_esperados}")
            else:
                patron_espaciado = r'\s*'.join(list(digitos_esperados))
                if re.search(patron_espaciado, texto):
                    resultados['exitos'].append(f"✅ La cédula {digitos_esperados} aparece en el RUT")
                else:
                    resultados['errores'].append(
                        f"❌ La cédula del RUT ({datos['numero_identificacion'] or 'no detectada'}) "
                        f"no coincide con la esperada ({digitos_esperados})"
                    )

        resultados['valido'] = len(resultados['errores']) == 0
        return resultados

    def generar_respuesta(self, resultados, contratista_info=None):
        """Genera una respuesta clara y concisa para el usuario"""
        lineas = []

        # Solo mostrar nombre si viene del sistema (no del RUT)
        if contratista_info and contratista_info.get('nombre'):
            lineas.append(f"👤 **Contratista:** {contratista_info['nombre']}")
            if contratista_info.get('cedula'):
                lineas.append(f"🆔 **Cédula:** {contratista_info['cedula']}")
            lineas.append("")

        # Veredicto final
        if resultados['valido']:
            lineas.append("✅ **¡Tu RUT está listo para subir a la plataforma!**")
        else:
            lineas.append("❌ **Tu RUT tiene problemas que debes corregir:**")

        lineas.append("")

        # Mostrar éxitos (cosas que están bien)
        if resultados['exitos']:
            for e in resultados['exitos']:
                lineas.append(f"  {e}")

        # Mostrar errores (cosas que están mal)
        if resultados['errores']:
            lineas.append("")
            for e in resultados['errores']:
                lineas.append(f"  {e}")

        # Mostrar advertencias
        if resultados['advertencias']:
            lineas.append("")
            lineas.append("⚠️ **Advertencias:**")
            for a in resultados['advertencias']:
                lineas.append(f"  {a}")

        # Consejos útiles si hay errores
        if not resultados['valido']:
            lineas.append("")
            lineas.append("📌 **¿Qué hacer?**")
            errores_texto = " ".join(resultados['errores']).lower()
            if any(p in errores_texto for p in ['trámite', 'tramite']):
                lineas.append("  • Espera a tener 'Actualización' o 'Copia', no 'En trámite'")
            if any(p in errores_texto for p in ['actividad', '8560']):
                lineas.append("  • Agrega actividad económica 8560 en la DIAN (educación)")
            if any(p in errores_texto for p in ['días', 'vigente', 'antiguo']):
                lineas.append("  • Saca un RUT actualizado (menos de 30 días de generación)")
            if any(p in errores_texto for p in ['cédula', 'cedula', 'coincide']):
                lineas.append("  • Verifica que el RUT sea tuyo y la cédula coincida")

        return "\n".join(lineas)


def validar_rut_archivo(ruta_pdf, cedula_contratista):
    from contratacion.lector import lector

    validador = ValidadorRUT()
    contratista_info = None
    if cedula_contratista:
        registros = lector.buscar_por_cedula(cedula_contratista)
        if registros:
            contratista_info = lector.obtener_info_contratista(registros[0])

    resultados = validador.analizar_rut(ruta_pdf, contratista_info, cedula_contratista)

    # Imprime en consola del servidor los datos leídos, en JSON, junto al análisis
    print("=" * 60)
    print("📄 DATOS EXTRAÍDOS DEL RUT (JSON)")
    print("=" * 60)
    print(json.dumps(resultados.get('datos_extraidos', {}), ensure_ascii=False, indent=2))
    print("=" * 60)

    respuesta = validador.generar_respuesta(resultados, contratista_info)
    return respuesta, resultados