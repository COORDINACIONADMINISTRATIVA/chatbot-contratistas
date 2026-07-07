"""
Validador / Lector de RUT (DIAN - Colombia)
=============================================

POR QUÉ ESTE ARCHIVO EXISTE ASÍ:
El texto que pypdf extrae de un RUT NO respeta el orden visual del PDF.
Todas las ETIQUETAS ("26. Número de Identificación", "42. Correo electrónico"...)
salen agrupadas en un bloque, y todos los VALORES salen agrupados en OTRO bloque,
varias líneas más abajo, en un orden distinto al de las etiquetas.

Por eso "buscar la etiqueta y leer lo que sigue" (la estrategia que fallaba antes)
nunca fue confiable. La estrategia correcta es reconocer los VALORES por su
FORMA (un correo tiene @, una fecha tiene guiones, una cédula es una tira de
10 dígitos separados por espacios, etc.) y por su POSICIÓN RELATIVA entre sí
(la dirección siempre queda una línea antes del correo, el teléfono una línea
después, etc.), no por la etiqueta que las precede.

Este módulo entrega:
- `extraer_datos_rut(texto)` -> dict JSON con todos los campos reconocidos.
- `ValidadorRUT.analizar_rut(...)` -> valida reglas de negocio (marca de agua,
  actividad económica, vigencia, cédula) usando esos datos.
"""
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
}


# ---------------------------------------------------------------------------
# Extracción de campos individuales (por FORMA, no por etiqueta)
# ---------------------------------------------------------------------------

def _extraer_tipo_documento(texto):
    for tipo in TIPOS_DOCUMENTO:
        if tipo.lower() in texto.lower():
            return tipo
    return None


def _extraer_cedula(texto, tipo_documento):
    """Cédula = tira de dígitos sueltos justo después del tipo de documento."""
    if tipo_documento:
        m = re.search(
            re.escape(tipo_documento) + r'\s+((?:\d\s*){6,10})',
            texto, re.IGNORECASE
        )
        if m:
            return re.sub(r'\D', '', m.group(1))
    # Fallback: cualquier tira de 6-10 dígitos sueltos con espacios entre cada uno
    m = re.search(r'\b(?:\d\s+){5,9}\d\b', texto)
    if m:
        return re.sub(r'\D', '', m.group())
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
    Busca líneas en MAYÚSCULA sostenida (2 a 6 palabras, sin dígitos) que no
    sean palabras clave del formulario. En un RUT esa línea es el nombre
    completo (persona natural) o la razón social (persona jurídica), y suele
    aparecer repetida (una vez en el bloque de identificación, otra en la
    firma al final del documento).
    """
    candidatos = {}
    for linea in _lineas_utiles(texto):
        if not linea or any(ch.isdigit() for ch in linea):
            continue
        palabras = linea.split()
        if not (2 <= len(palabras) <= 6):
            continue
        if not all(re.fullmatch(r'[A-ZÁÉÍÓÚÑ]+', p) for p in palabras):
            continue
        primera = palabras[0]
        if primera in PALABRAS_NO_NOMBRE:
            continue
        candidatos[linea] = candidatos.get(linea, 0) + 1

    if not candidatos:
        return None, {}

    # el nombre real suele repetirse (aparece también en la firma)
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
                break  # ya pasamos la dirección, no hay dirección legible
            direccion = candidata
            break

        # Teléfonos: siguiente línea con dígitos
        for j in range(idx_correo + 1, min(idx_correo + 3, len(lineas))):
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
    [código 4 dígitos][fecha AAAAMMDD 8 dígitos] pegados, validando que la
    fecha sea real antes de aceptar el código (esto evita confundir números
    de teléfono con actividades económicas, que era el bug anterior).
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
    m = re.search(
        r'Fecha\s*generaci[oó]n\s*documento\s*PDF:?\s*(\d{1,2})-(\d{1,2})-(\d{4})\s*(\d{1,2}:\d{2}:\d{2}\s*[AP]M)?',
        texto, re.IGNORECASE
    )
    if not m:
        return None
    d, mo, y, hora = m.groups()
    try:
        fecha = datetime(int(y), int(mo), int(d))
    except ValueError:
        return None
    return {'fecha': fecha.strftime('%d/%m/%Y'), 'hora': hora, '_dt': fecha}


def _extraer_fecha_actualizacion(texto):
    """Formato distinto al anterior: AAAA-MM-DD / HH:MM:SSPM."""
    m = re.search(r'(\d{4})-(\d{2})-(\d{2})\s*/\s*(\d{1,2}:\d{2}:\d{2}\s*[AP]M)', texto)
    if not m:
        return None
    y, mo, d, hora = m.groups()
    try:
        fecha = datetime(int(y), int(mo), int(d))
    except ValueError:
        return None
    return {'fecha': fecha.strftime('%d/%m/%Y'), 'hora': hora, '_dt': fecha}


def _extraer_marca_agua(texto):
    t = texto.lower()
    if 'en trámite' in t or 'en tramite' in t:
        return 'en_tramite', "El RUT dice 'EN TRÁMITE' (no sirve todavía)"
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
        fecha_actualizacion['_dt'] if fecha_actualizacion else
        (fecha_generacion['_dt'] if fecha_generacion else None)
    )
    return datos


# ---------------------------------------------------------------------------
# Validación de reglas de negocio (lo que ya tenías, ahora sobre datos limpios)
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
        datos_publicos = {k: v for k, v in datos.items() if not k.startswith('_')}
        resultados['datos_extraidos'] = datos_publicos

        # --- Marca de agua ---
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

        # --- Vigencia (usa fecha de actualización si existe, si no la de generación del PDF) ---
        fecha_dt = datos['_fecha_referencia_dt']
        if fecha_dt:
            dias = (datetime.now() - fecha_dt).days
            if dias <= 30:
                resultados['exitos'].append(f"✅ RUT vigente, expedido/actualizado hace {dias} días")
            elif dias <= 365:
                resultados['advertencias'].append(f"⚠️ El RUT tiene {dias} días. Revisa si tu proceso exige menos de 30 días")
            else:
                resultados['errores'].append(f"❌ El RUT es muy antiguo ({dias} días)")
        else:
            resultados['advertencias'].append("⚠️ No se pudo leer ninguna fecha del documento")

        # --- Cédula: se VERIFICA contra la que ya conocemos, no se confía solo en lo leído ---
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
        lineas = ["📄 **Análisis de tu RUT**\n"]
        if contratista_info:
            if contratista_info.get('nombre'):
                lineas.append(f"👤 **Nombre (en el sistema):** {contratista_info['nombre']}")
            if contratista_info.get('cedula'):
                lineas.append(f"🆔 **Cédula (en el sistema):** {contratista_info['cedula']}")
            lineas.append("")

        datos = resultados.get('datos_extraidos', {})
        if datos:
            lineas.append("📋 **Datos leídos del PDF:**")
            if datos.get('nombre_completo'):
                lineas.append(f"• Nombre/Razón social: {datos['nombre_completo']}")
            if datos.get('numero_identificacion'):
                lineas.append(f"• Identificación: {datos['numero_identificacion']}")
            if datos.get('correo'):
                lineas.append(f"• Correo: {datos['correo']}")
            if datos.get('telefonos'):
                lineas.append(f"• Teléfono(s): {', '.join(datos['telefonos'])}")
            if datos.get('direccion'):
                lineas.append(f"• Dirección: {datos['direccion']}")
            if datos.get('actividades_economicas'):
                acts = ', '.join(f"{a['codigo']} ({a['fecha_inicio']})" for a in datos['actividades_economicas'])
                lineas.append(f"• Actividad(es) económica(s): {acts}")
            if datos.get('responsabilidades_calidades_atributos'):
                lineas.append(f"• Responsabilidades: {', '.join(datos['responsabilidades_calidades_atributos'])}")
            if datos.get('fecha_actualizacion_rut'):
                lineas.append(f"• Fecha actualización RUT: {datos['fecha_actualizacion_rut']}")
            if datos.get('fecha_generacion_pdf'):
                lineas.append(f"• Fecha generación PDF: {datos['fecha_generacion_pdf']}")
            lineas.append("")

        if resultados['valido']:
            lineas.append("✅ **¡Tu RUT está listo para subir!**\n")
            for e in resultados['exitos']:
                lineas.append(f"  {e}")
        else:
            lineas.append("❌ **Tu RUT tiene problemas:**\n")
            for e in resultados['errores']:
                lineas.append(f"  {e}")
            if resultados['advertencias']:
                lineas.append("\n⚠️ **Advertencias:**")
                for a in resultados['advertencias']:
                    lineas.append(f"  {a}")

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
