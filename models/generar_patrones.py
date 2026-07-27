"""
Generador de patrones para el chatbot de contratistas
Este script toma las frases base y genera variaciones automáticamente
para triplicar o cuadruplicar los patrones del chatbot.
"""

import json
import random
import re
from datetime import datetime

# ==================== CONFIGURACIÓN ====================
ARCHIVO_FAQS = 'knowledge_base/faqs_contratista.json'
ARCHIVO_SALIDA = 'knowledge_base/faqs_contratista_generado.json'

# ==================== DICCIONARIO DE VARIACIONES ====================
VARIACIONES = {
    # Verbos comunes
    'subir': ['subir', 'mandar', 'enviar', 'cargar', 'adjuntar', 'poner', 'agregar', 'entregar'],
    'registrar': ['registrar', 'inscribir', 'matricular', 'anotar', 'apuntar', 'crear'],
    'actualizar': ['actualizar', 'renovar', 'cambiar', 'modificar', 'arreglar', 'corregir', 'sacar nuevo'],
    'validar': ['validar', 'verificar', 'revisar', 'analizar', 'chequear', 'confirmar'],
    
    # Sustantivos
    'documentos': ['documentos', 'papeles', 'papelería', 'requisitos', 'anexos', 'archivos', 'formatos'],
    'portal': ['portal', 'plataforma', 'sistema', 'página', 'sitio', 'aplicación', 'programa'],
    'rut': ['rut', 'RUT', 'r.u.t', 'R.U.T', 'ese documento', 'el rut ese'],
    'registro': ['registro', 'inscripción', 'matrícula', 'creación de cuenta', 'alta'],
    'sede': ['sede', 'oficina', 'ubicación', 'lugar', 'dirección'],
    'regimen': ['regimen', 'régimen', 'tipo de contribuyente', 'régimen tributario'],
    'tratamiento': ['tratamiento', 'título', 'forma de trato', 'señor o señora'],
    'codigo postal': ['código postal', 'codigo postal', 'código', 'zip code', 'codigo de área'],
    
    # Verbos auxiliares
    'ayuda_verbo': ['ayuda con', 'ayuda para', 'necesito', 'quiero', 'como hago', 'como puedo', 'me puedes'],
    'problema_verbo': ['no puedo', 'no me deja', 'no funciona', 'me sale error', 'se traba', 'no carga'],
    
    # Preguntas
    'pregunta': ['como', 'donde', 'cuando', 'por que', 'para que', 'cual', 'que', 'quien'],
}

# ==================== FUNCIONES AUXILIARES ====================

def limpiar_texto(texto):
    """Limpia el texto de caracteres especiales y espacios extra"""
    texto = re.sub(r'\s+', ' ', texto)
    return texto.strip()

def generar_variacion(frase, variaciones, max_variaciones=100):
    """
    Genera variaciones de una frase usando el diccionario de variaciones.
    """
    frase_original = frase
    frases_generadas = [frase_original]
    
    # Reemplazar palabras clave por sus sinónimos
    for palabra_clave, sinonimos in variaciones.items():
        # Si la palabra clave está en la frase
        if palabra_clave in frase_original.lower():
            # Generar nuevas frases reemplazando esa palabra
            for sinonimo in sinonimos:
                if sinonimo != palabra_clave:
                    nueva_frase = frase_original.replace(palabra_clave, sinonimo)
                    if nueva_frase not in frases_generadas and len(nueva_frase) < 100:
                        frases_generadas.append(nueva_frase)
    
    # Si no se generaron suficientes, agregar variaciones con prefijos/sufijos
    if len(frases_generadas) < 3:
        prefijos = ['ayuda con ', 'necesito ', 'quiero ', 'como hago para ']
        sufijos = [' por favor', ' ayuda', ' urgente']
        
        for prefijo in prefijos:
            nueva = prefijo + frase_original
            if nueva not in frases_generadas and len(nueva) < 100:
                frases_generadas.append(nueva)
        
        for sufijo in sufijos:
            nueva = frase_original + sufijo
            if nueva not in frases_generadas and len(nueva) < 100:
                frases_generadas.append(nueva)
    
    # Convertir a minúsculas, limpiar y eliminar duplicados
    frases_generadas = [limpiar_texto(f.lower()) for f in frases_generadas]
    frases_generadas = list(set(frases_generadas))
    
    # Limitar el número de variaciones
    return frases_generadas[:max_variaciones]

def generar_patrones_mejorados(intents, factor=3):
    """
    Toma los intents existentes y genera más patrones para cada uno.
    factor: cuántas veces más patrones generar (ej: 3 = triple)
    """
    nuevos_intents = []
    
    for intent in intents:
        tag = intent['tag']
        patrones_originales = intent['patrones']
        
        # Generar nuevas variaciones para cada patrón
        nuevos_patrones = []
        for patron in patrones_originales:
            variaciones = generar_variacion(patron, VARIACIONES, max_variaciones=10)
            nuevos_patrones.extend(variaciones)
        
        # Combinar patrones originales + nuevos
        todos_patrones = list(set(patrones_originales + nuevos_patrones))
        
        # Crear el intent mejorado
        nuevo_intent = {
            'tag': tag,
            'patrones': todos_patrones
        }
        
        nuevos_intents.append(nuevo_intent)
        
        print(f"✅ {tag}: {len(patrones_originales)} -> {len(todos_patrones)} patrones")
    
    return nuevos_intents

def guardar_json(data, archivo):
    """Guarda los datos en un archivo JSON"""
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"📁 Archivo guardado: {archivo}")

def cargar_json(archivo):
    """Carga un archivo JSON"""
    with open(archivo, 'r', encoding='utf-8') as f:
        return json.load(f)

# ==================== EJECUCIÓN PRINCIPAL ====================

def main():
    print("=" * 60)
    print("🚀 GENERADOR DE PATRONES PARA CHATBOT")
    print("=" * 60)
    
    # Cargar el archivo actual
    try:
        data = cargar_json(ARCHIVO_FAQS)
        intents = data['intents']
        print(f"📊 Cargados {len(intents)} intents con {sum(len(i['patrones']) for i in intents)} patrones")
    except FileNotFoundError:
        print(f"❌ No se encontró el archivo: {ARCHIVO_FAQS}")
        return
    
    # Generar nuevos patrones
    print("\n🔄 Generando patrones...")
    nuevos_intents = generar_patrones_mejorados(intents, factor=3)
    
    # Crear el nuevo JSON
    nuevo_data = {'intents': nuevos_intents}
    
    # Guardar el archivo generado
    guardar_json(nuevo_data, ARCHIVO_SALIDA)
    
    # Estadísticas finales
    total_original = sum(len(i['patrones']) for i in intents)
    total_nuevo = sum(len(i['patrones']) for i in nuevos_intents)
    
    print("\n" + "=" * 60)
    print("📊 ESTADÍSTICAS FINALES")
    print("=" * 60)
    print(f"📌 Patrones originales: {total_original}")
    print(f"📌 Patrones generados: {total_nuevo}")
    print(f"📌 Incremento: {total_nuevo - total_original} patrones ({round(total_nuevo/total_original, 1)}x)")
    print("=" * 60)
    print(f"\n✅ Archivo generado: {ARCHIVO_SALIDA}")
    print("📌 Revisa el archivo y si está bien, renómbralo a faqs_contratista.json")
    print("📌 Luego ejecuta: python -m models.entrenar_modelo")

if __name__ == '__main__':
    main()