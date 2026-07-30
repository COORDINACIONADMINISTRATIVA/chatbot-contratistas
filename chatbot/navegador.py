# chatbot/navegador.py
"""
Manejador de comandos de navegación: siguiente, atrás, menú, ayuda
"""

import re
from .flujos import (
    obtener_flujo, obtener_paso, total_pasos, es_paso_final,
    obtener_titulo_flujo, obtener_mensaje_final
)

# ============================================================
# DETECCIÓN DE COMANDOS
# ============================================================

def es_comando_siguiente(texto):
    """Detecta si el usuario quiere avanzar al siguiente paso"""
    t = texto.lower()
    comandos = ['siguiente', 'siguiente paso', 'siguiente paso', 'avanzar', 
                'adelante', 'continuar', 'siguiente tema', 'siguiente sección',
                'si', 'sí', 'ok', 'vale', 'bueno', 'claro', 'listo', 'adelante']
    return any(c in t for c in comandos)

def es_comando_atras(texto):
    """Detecta si el usuario quiere retroceder al paso anterior"""
    t = texto.lower()
    comandos = ['atrás', 'atras', 'volver', 'regresar', 'retroceder', 
                'anterior', 'paso atrás', 'paso atras', 'back']
    return any(c in t for c in comandos)

def es_comando_ayuda(texto):
    """Detecta si el usuario quiere más información sobre el paso actual"""
    t = texto.lower()
    comandos = ['ayuda', 'ayudame', 'explica', 'explícame', 'detalle', 
                'más info', 'mas info', 'no entiendo', 'duda', 'explicame']
    return any(c in t for c in comandos)

def es_comando_menu(texto):
    """Detecta si el usuario quiere volver al menú principal"""
    t = texto.lower()
    comandos = ['menú', 'menu', 'inicio', 'principal', 'volver al menú', 
                'volver al menu', 'home', 'empezar de nuevo', 'reset']
    return any(c in t for c in comandos)

def es_comando_salir(texto):
    """Detecta si el usuario quiere terminar la conversación"""
    t = texto.lower()
    comandos = ['salir', 'terminar', 'finalizar', 'chao', 'adios', 'bye', 
                'gracias', 'hasta luego', 'nos vemos']
    return any(c in t for c in comandos)

def es_numero_menu(texto, opciones):
    """Detecta si el usuario seleccionó una opción por número"""
    match = re.match(r'^(\d+)$', texto.strip())
    if not match:
        return None
    num = int(match.group(1))
    if 1 <= num <= len(opciones):
        return num - 1
    return None

# ============================================================
# FORMATEADORES DE MENSAJES
# ============================================================

def formatear_paso(flujo_id, paso, indice, total):
    """Formatea un paso para mostrarlo al usuario con navegación"""
    titulo = paso.get('titulo', f'Paso {indice + 1}')
    contenido = paso.get('contenido', '')
    pregunta = paso.get('pregunta', '')
    opciones = paso.get('opciones', [])
    
    # Barra de progreso simple
    progreso = f"📌 Paso {indice + 1} de {total}"
    
    mensaje = f"""📌 {titulo} {progreso}

{contenido}

💡 {pregunta}"""
    
    # Agregar opciones numeradas
    if opciones:
        mensaje += "\n\n"
        for i, opcion in enumerate(opciones, 1):
            # Limpiar números o emojis de las opciones
            opcion_limpia = re.sub(r'^[\d\.]+\s*', '', opcion)
            opcion_limpia = re.sub(r'^[✅❌📌📍🔄📋📤🔐🆘🔍]+\s*', '', opcion_limpia)
            mensaje += f"{i}. {opcion_limpia}\n"
    
    # Agregar comandos de navegación (más limpio)
    mensaje += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
▶️ Escriba el número de la opción o use un comando:
◀️ atrás   ℹ️ ayuda   🏠 menú
"""
    return mensaje

def formatear_detalle(paso):
    """Formatea el detalle de un paso"""
    detalle = paso.get('detalle', '')
    if not detalle:
        return "No hay información adicional disponible."
    
    return f"""📖 DETALLE

{detalle}

ℹ️ ¿Necesita más información o quiere continuar?
▶️ "siguiente" - Avanzar
◀️ "atrás" - Retroceder
🏠 "menú" - Volver al inicio
"""

def formatear_menu_principal():
    """Formatea el menú principal"""
    return """👋 ¡Hola! Soy tu asistente de contratación de UNIMINUTO Virtual.

Estoy aquí para guiarte paso a paso en todo el proceso de contratación: desde el registro en el portal hasta la firma de tu contrato.

📌 Elige un tema escribiendo el número o el nombre:

1️⃣ 📋 Documentos requeridos
2️⃣ 🌐 Registro en el portal de proveedores
3️⃣ 📝 Actualización del RUT
4️⃣ 🏥 ARL (Afiliación y certificación)
5️⃣ 🏥 Examen médico ocupacional
6️⃣ 📊 Estado de mi proceso

¿En qué puedo ayudarte hoy?
"""

def formatear_despedida():
    """Formatea el mensaje de despedida"""
    return """👋 ¡Hasta luego!

Si necesita ayuda más adelante, vuelva a escribir.
Recuerde que estoy aquí para apoyarle en su proceso de contratación.

¿Quiere hacer alguna otra consulta?
"""

def formatear_error(comando):
    """Formatea un mensaje de error para comandos no reconocidos"""
    return f"""❌ No entendí "{comando}".

Puede usar:
▶️ "siguiente" - Para avanzar al siguiente paso
◀️ "atrás" - Para retroceder al paso anterior
ℹ️ "ayuda" - Para más información sobre el paso actual
🏠 "menú" - Para volver al menú principal

¿Qué desea hacer?
"""