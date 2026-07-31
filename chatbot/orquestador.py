# chatbot/orquestador.py
"""
Punto de entrada único del chatbot con sistema de flujo guiado
VERSIÓN DEFINITIVA - Maneja respuestas "No" con detalles y redirige a ayuda externa
"""

from .gestor_estado import gestor
from .flujos import obtener_flujo, obtener_paso, total_pasos, es_paso_final, obtener_mensaje_final
from .navegador import (
    es_comando_siguiente, es_comando_atras, es_comando_ayuda, 
    es_comando_menu, es_comando_salir,
    formatear_paso, formatear_detalle, formatear_menu_principal,
    formatear_despedida, formatear_error
)
from .detector import extraer_cedula
from .memoria import memoria
from .respuestas import RESPUESTAS


# ============================================================
# MAPEO DE PALABRAS CLAVE A FLUJOS
# ============================================================
MAP_TEMAS = {
    "documentos": "documentos_natural",
    "documentacion": "documentos_natural",
    "documento": "documentos_natural",
    "papeles": "documentos_natural",
    "requisitos": "documentos_natural",
    "registro": "registro",
    "portal": "registro",
    "proveedores": "registro",
    "plataforma": "registro",
    "inscribirme": "registro",
    "rut": "rut_actualizar",
    "actualizar rut": "rut_actualizar",
    "renovar rut": "rut_actualizar",
    "arl": "arl",
    "afiliarme": "arl",
    "examen medico": "examen_medico",
    "examen": "examen_medico",
    "medico": "examen_medico",
    "estado": "estado",
    "mi proceso": "estado",
    "proceso": "estado",
}

import re
import unicodedata

TEMAS_NUMEROS = ["documentos", "registro", "rut", "arl", "examen"]

_STOPWORDS = {
    'ya', 'lo', 'la', 'el', 'de', 'que', 'no', 'si', 'a', 'en', 'un', 'una',
    'tengo', 'esta', 'con', 'para', 'mi', 'me', 'del', 'al', 'es', 'y', 'o', 'su'
}


def _quitar_tildes(texto):
    """Normaliza tildes: 'dónde' -> 'donde' (muy común que el usuario escriba sin acentos)"""
    nfkd = unicodedata.normalize('NFKD', texto)
    return ''.join(c for c in nfkd if not unicodedata.combining(c))


def _normalizar(texto):
    """Quita emojis/puntuación/tildes y deja solo palabras en minúscula"""
    texto = _quitar_tildes(texto.lower())
    texto = re.sub(r'[^\w\s]', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto


def detectar_opcion_por_texto(mensaje_lower, opciones):
    """
    Intenta mapear una respuesta en texto libre (ej. 'estoy esperando el resultado')
    a una de las opciones numeradas del paso actual, comparando palabras clave.
    Devuelve el número de opción (1-indexed) o None si no hay coincidencia clara.
    """
    if not opciones:
        return None
    msg_norm = _normalizar(mensaje_lower)
    msg_palabras = set(msg_norm.split()) - _STOPWORDS
    if not msg_palabras:
        return None

    mejor_indice, mejor_score = None, 0
    for i, opcion in enumerate(opciones):
        op_norm = _normalizar(opcion)
        op_palabras = set(op_norm.split()) - _STOPWORDS
        if not op_palabras:
            continue
        score = len(msg_palabras & op_palabras)
        if msg_norm and (msg_norm in op_norm or op_norm in msg_norm):
            score += 2
        if score > mejor_score:
            mejor_score, mejor_indice = score, i

    if mejor_indice is not None and mejor_score >= 1:
        return mejor_indice + 1
    return None


def detectar_tema(mensaje):
    mensaje_lower = mensaje.lower()
    for palabra, flujo_id in MAP_TEMAS.items():
        if palabra in mensaje_lower:
            return flujo_id
    return None


def es_numero(texto):
    try:
        num = int(texto.strip())
        return 1 <= num <= 20, num
    except:
        return False, None


def _es_lista_de_seleccion(opciones):
    """
    True si las opciones son una lista de temas distintos a los que 'saltar'
    (ej: '1. Cédula', '2. Certificación bancaria'...), en vez de un Sí/No simple
    donde cualquier respuesta debe avanzar un solo paso.
    """
    if len(opciones) < 2:
        return False
    numeradas = sum(1 for o in opciones if re.match(r'^\d+\.\s', o.strip()))
    # Todas (o todas menos la de "volver al menú") deben venir numeradas
    return numeradas >= len(opciones) - 1 and numeradas >= 2


def es_opcion_volver_menu(texto):
    t = texto.lower()
    return "volver al menú" in t or "volver al menu" in t or "🏠" in texto or "ir al menú principal" in t


def es_opcion_volver_inicio_flujo(texto):
    """
    Para opciones como '🔙 Volver a documentos': el usuario quiere regresar
    al paso 0 (la lista/intro) del flujo ACTUAL, no salir al menú principal.
    """
    t = texto.lower()
    return "volver" in t and not es_opcion_volver_menu(texto)


def responder(mensaje, usuario="anonimo"):
    mensaje_limpio = mensaje.strip()
    mensaje_lower = mensaje_limpio.lower()

    # SALUDOS
    saludos = ['hola', 'ola', 'buenos', 'buenas', 'hi', 'hello', 'buen día', 'buenas tardes']
    if any(s in mensaje_lower for s in saludos) and len(mensaje_limpio) < 60:
        tema = detectar_tema(mensaje_limpio)
        if tema:
            return iniciar_flujo(usuario, tema, mensaje)
        return formatear_menu_principal()

    # SI CON [TEMA]
    if mensaje_lower.startswith("si") or mensaje_lower.startswith("sí"):
        for tema in ["documentos", "rut", "arl", "examen", "portal", "registro"]:
            if tema in mensaje_lower:
                return iniciar_flujo(usuario, tema, mensaje)

    # CAMBIO DE TEMA
    tema_detectado = detectar_tema(mensaje_limpio)
    if tema_detectado and gestor.esta_en_flujo(usuario):
        gestor.resetear(usuario)
        return iniciar_flujo(usuario, tema_detectado, mensaje)

    # Guardar mensaje
    memoria.guardar_mensaje(usuario, mensaje, tipo="usuario")
    estado = gestor.obtener_estado(usuario)

    # ============================================================
    # SI ESTÁ EN UN FLUJO
    # ============================================================
    if gestor.esta_en_flujo(usuario):
        flujo_id = estado['flujo']
        paso_actual = estado['paso']
        total = total_pasos(flujo_id)
        paso = obtener_paso(flujo_id, paso_actual)
        opciones = paso.get('opciones', []) if paso else []

        # --- COMANDOS ---
        if es_comando_salir(mensaje_limpio):
            respuesta = formatear_despedida()
            gestor.resetear(usuario)
            memoria.guardar_mensaje(usuario, respuesta, tipo="bot")
            return respuesta

        if es_comando_menu(mensaje_limpio):
            respuesta = formatear_menu_principal()
            gestor.resetear(usuario)
            memoria.guardar_mensaje(usuario, respuesta, tipo="bot")
            return respuesta

        if es_comando_atras(mensaje_limpio):
            if paso_actual > 0:
                gestor.retroceder_paso(usuario)
                nuevo_paso = obtener_paso(flujo_id, estado['paso'])
                respuesta = formatear_paso(flujo_id, nuevo_paso, estado['paso'], total)
            else:
                respuesta = "⚠️ Ya estás en el primer paso."
            memoria.guardar_mensaje(usuario, respuesta, tipo="bot")
            return respuesta

        if es_comando_ayuda(mensaje_limpio) and paso:
            respuesta = formatear_detalle(paso)
            memoria.guardar_mensaje(usuario, respuesta, tipo="bot")
            return respuesta

        # ============================================================
        # SELECCIÓN DE OPCIÓN POR NÚMERO
        # ============================================================
        es_num, num = es_numero(mensaje_limpio)

        # Si no escribió un número, intentar reconocer texto libre como opción
        # (ej: "estoy esperando el resultado" -> opción "⏳ Estoy esperando el resultado")
        if not es_num and opciones:
            num_texto = detectar_opcion_por_texto(mensaje_lower, opciones)
            if num_texto:
                es_num, num = True, num_texto

        # ============================================================
        # CASO ESPECIAL: RESPUESTA "NO" CON DETALLE Y REDIRECCIÓN
        # ============================================================
        # Solo se activa si el paso NO es una lista de selección
        if paso and paso.get('respuesta_no') and not _es_lista_de_seleccion(opciones):
            if es_num and num == 2:
                # Verificar si ya se mostró la ayuda detallada
                ultima_respuesta = memoria.obtener_ultima_respuesta(usuario)
                
                # Si la última respuesta contenía la pregunta de seguimiento, ya se mostró la ayuda
                if ultima_respuesta and ('✅ Sí, entendí' in ultima_respuesta or '❌ No, aún tengo dudas' in ultima_respuesta):
                    # Redirigir al paso de ayuda externa (el último paso del flujo)
                    paso_destino = total - 1  # El último paso es ayuda_externa
                    gestor.ir_a_paso(usuario, paso_destino)
                    nuevo_paso = obtener_paso(flujo_id, estado['paso'])
                    respuesta = formatear_paso(flujo_id, nuevo_paso, estado['paso'], total)
                    memoria.guardar_mensaje(usuario, respuesta, tipo="bot")
                    return respuesta
                else:
                    # Mostrar la ayuda detallada por primera vez
                    respuesta_no = paso['respuesta_no']
                    mensaje_detalle = respuesta_no.get('mensaje', '')
                    pregunta_seguimiento = respuesta_no.get('pregunta', '¿Entendió la explicación?')
                    opciones_seguimiento = respuesta_no.get('opciones', ['✅ Sí, entendí', '❌ No, aún tengo dudas'])
                    
                    respuesta = f"{mensaje_detalle}\n\n💡 {pregunta_seguimiento}\n\n"
                    for i, op in enumerate(opciones_seguimiento, 1):
                        respuesta += f"{i}. {op}\n"
                    
                    memoria.guardar_mensaje(usuario, respuesta, tipo="bot")
                    return respuesta

        # ============================================================
        # SELECCIÓN DE OPCIÓN POR NÚMERO (CONTINUACIÓN)
        # ============================================================
        if es_num and paso_actual == 0 and num <= len(opciones) and _es_lista_de_seleccion(opciones):
            # Este paso es una LISTA de temas distintos a los que saltar
            # (ej: "1. Cédula", "2. Certificación bancaria"...), no un Sí/No simple.
            opcion_seleccionada = opciones[num - 1]

            # Si el texto de la opción elegida es "volver al menú", volver directo
            if es_opcion_volver_menu(opcion_seleccionada):
                respuesta = formatear_menu_principal()
                gestor.resetear(usuario)
                memoria.guardar_mensaje(usuario, respuesta, tipo="bot")
                return respuesta

            # La opción N corresponde directamente al paso N
            # (paso 0 = intro/lista, paso 1 = primer tema, paso 2 = segundo, etc.)
            paso_destino = num

            # Verificar que el paso destino existe
            if paso_destino < total:
                gestor.guardar_dato(usuario, f"paso_{paso_actual}", opcion_seleccionada)
                
                # Saltar al paso destino
                gestor.ir_a_paso(usuario, paso_destino)
                nuevo_paso = obtener_paso(flujo_id, estado['paso'])
                respuesta = formatear_paso(flujo_id, nuevo_paso, estado['paso'], total)
                memoria.guardar_mensaje(usuario, respuesta, tipo="bot")
                return respuesta
            else:
                respuesta = formatear_error(mensaje_limpio)
                memoria.guardar_mensaje(usuario, respuesta, tipo="bot")
                return respuesta

        elif es_num and 1 <= num <= len(opciones):
            # OTROS PASOS (o Sí/No en el paso 0): el usuario eligió una opción (1, 2, 3)
            # y simplemente se avanza un paso, sin importar cuál haya elegido.
            opcion_seleccionada = opciones[num - 1]
            gestor.guardar_dato(usuario, f"paso_{paso_actual}", opcion_seleccionada)
            
            # Verificar si es "volver al menú" (sale del flujo por completo)
            if es_opcion_volver_menu(opcion_seleccionada):
                respuesta = formatear_menu_principal()
                gestor.resetear(usuario)
                memoria.guardar_mensaje(usuario, respuesta, tipo="bot")
                return respuesta

            # Verificar si la opción es "Ir al menú principal"
            if "ir al menú principal" in opcion_seleccionada.lower():
                respuesta = formatear_menu_principal()
                gestor.resetear(usuario)
                memoria.guardar_mensaje(usuario, respuesta, tipo="bot")
                return respuesta

            # Verificar si es "volver a documentos" / "volver al tema" (regresa al
            # paso 0 del MISMO flujo, no sale al menú principal)
            if es_opcion_volver_inicio_flujo(opcion_seleccionada):
                gestor.ir_a_paso(usuario, 0)
                nuevo_paso = obtener_paso(flujo_id, 0)
                respuesta = formatear_paso(flujo_id, nuevo_paso, 0, total)
                memoria.guardar_mensaje(usuario, respuesta, tipo="bot")
                return respuesta
            
            # Verificar si es el último paso
            if es_paso_final(flujo_id, paso_actual):
                respuesta = obtener_mensaje_final(flujo_id) or "✅ ¡Has completado este tema!"
                gestor.resetear(usuario)
                memoria.guardar_mensaje(usuario, respuesta, tipo="bot")
                return respuesta
            
            # Avanzar al siguiente paso
            gestor.avanzar_paso(usuario)
            nuevo_paso = obtener_paso(flujo_id, estado['paso'])
            respuesta = formatear_paso(flujo_id, nuevo_paso, estado['paso'], total)
            memoria.guardar_mensaje(usuario, respuesta, tipo="bot")
            return respuesta

        # Comando "siguiente"
        if es_comando_siguiente(mensaje_limpio):
            if es_paso_final(flujo_id, paso_actual):
                respuesta = obtener_mensaje_final(flujo_id) or "✅ ¡Has completado este tema!"
                gestor.resetear(usuario)
            else:
                gestor.avanzar_paso(usuario)
                nuevo_paso = obtener_paso(flujo_id, estado['paso'])
                respuesta = formatear_paso(flujo_id, nuevo_paso, estado['paso'], total)
            memoria.guardar_mensaje(usuario, respuesta, tipo="bot")
            return respuesta

        # Mensaje no reconocido
        respuesta = formatear_error(mensaje_limpio)
        memoria.guardar_mensaje(usuario, respuesta, tipo="bot")
        return respuesta

    # ============================================================
    # MENÚ PRINCIPAL (PRIORIDAD ALTA)
    # ============================================================
    if mensaje_limpio in ["1", "2", "3", "4", "5", "6"]:
        index = int(mensaje_limpio) - 1
        if 0 <= index < len(TEMAS_NUMEROS):
            return iniciar_flujo(usuario, TEMAS_NUMEROS[index], mensaje)

    # ============================================================
    # DETECCIÓN DE TEMAS (SOLO SI NO ES NÚMERO)
    # ============================================================
    tema_detectado = detectar_tema(mensaje_limpio)
    if tema_detectado:
        return iniciar_flujo(usuario, tema_detectado, mensaje)

    respuesta = formatear_menu_principal()
    memoria.guardar_mensaje(usuario, respuesta, tipo="bot")
    return respuesta


def iniciar_flujo(usuario, tema, mensaje=""):
    # 'tema' puede llegar ya resuelto como flujo_id (ej. "documentos_natural",
    # devuelto por detectar_tema) o como palabra clave cruda (ej. "documentos",
    # usada en TEMAS_NUMEROS y en el bloque "SI CON [TEMA]"). Se soportan ambos casos.
    flujo_id = tema if obtener_flujo(tema) else MAP_TEMAS.get(tema)
    if not flujo_id:
        return formatear_menu_principal()

    if flujo_id == "estado":
        cedula = extraer_cedula(mensaje)
        if not cedula:
            return "📋 Para consultar el estado de su proceso, escriba su número de cédula.\n\nEjemplo: 1234567890"
        return "🔍 Buscando información para la cédula " + cedula + "..."

    gestor.iniciar_flujo(usuario, flujo_id)
    paso = obtener_paso(flujo_id, 0)
    total = total_pasos(flujo_id)

    respuesta = formatear_paso(flujo_id, paso, 0, total)
    memoria.guardar_mensaje(usuario, respuesta, tipo="bot")
    return respuesta