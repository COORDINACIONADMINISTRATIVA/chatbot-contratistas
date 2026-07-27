# chatbot/contexto.py
"""
Detector de contexto: analiza el mensaje y determina el tema actual
"""
import re
from .normalizador import normalizar

# Palabras clave por tema
TEMAS = {
    'rut': ['rut', 'r.u.t', 'registro unico tributario', 'actualizar rut', 'renovar rut', 'rut nuevo'],
    'documentos': ['documentos', 'papeles', 'requisitos', 'certificacion', 'cedula', 'examen medico'],
    'portal': ['portal', 'proveedores', 'registro', 'plataforma', 'inscribir', 'registrarme'],
    'contrato': ['contrato', 'firma', 'firmar', 'vinculacion', 'prestacion'],
    'pagos': ['pago', 'pagar', 'factura', 'cuenta de cobro', 'honorarios'],
    'seguimiento': ['seguimiento', 'estado', 'proceso', 'avance', 'como va'],
}

def detectar_tema(texto):
    """
    Detecta el tema principal del mensaje
    """
    texto_norm = normalizar(texto)
    
    for tema, palabras in TEMAS.items():
        for palabra in palabras:
            if palabra in texto_norm:
                return tema
    
    # Si no se detecta un tema específico, usar el tema anterior o 'general'
    return 'general'

def extraer_entidades(texto):
    """
    Extrae entidades del texto (cédula, nombres, correos, etc.)
    """
    entidades = {}
    
    # Extraer cédula (6 a 12 dígitos)
    cedula_match = re.search(r'\b(\d{6,12})\b', texto)
    if cedula_match:
        entidades['cedula'] = cedula_match.group(1)
    
    # Extraer correo
    correo_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', texto)
    if correo_match:
        entidades['correo'] = correo_match.group(0)
    
    # Extraer nombre (palabras con mayúsculas, mínimo 2 palabras)
    nombre_match = re.search(r'([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)+)', texto)
    if nombre_match:
        entidades['nombre'] = nombre_match.group(0)
    
    return entidades