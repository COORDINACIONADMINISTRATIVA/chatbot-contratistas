# chatbot/detector.py
"""
Detector de intenciones para el chatbot
"""
import re

def extraer_cedula(texto):
    """Extrae un número de cédula de 6 a 12 dígitos del texto"""
    matches = re.findall(r'\b\d{6,12}\b', texto)
    for m in matches:
        if len(m) >= 7:
            return m
        if len(m) >= 6 and not m.startswith('20'):
            return m
    return None

def detectar_intencion(texto):
    """
    Detecta la intención del mensaje del usuario (para fallback del flujo)
    Si el usuario no está en un flujo, detecta qué quiere
    """
    t = texto.lower()
    cedula = extraer_cedula(texto)
    
    # Si hay cédula, es consulta de estado
    if cedula:
        return 'consulta_estado', cedula
    
    # RUT
    if 'rut' in t:
        if any(p in t for p in ['crear', 'hacer', 'obtener', 'sacar', 'conseguir', 'no tengo', 'nunca', 'primera vez']):
            return 'crear_rut', cedula
        if any(p in t for p in ['actualizar', 'renovar', 'cambiar', 'modificar', 'vencido']):
            return 'actualizar_rut', cedula
        return 'rut', cedula
    
    # ARL
    if any(p in t for p in ['arl', 'afiliarme', 'riesgos laborales']):
        return 'arl', cedula
    
    # Documentos
    if any(p in t for p in ['documentos', 'papeles', 'requisitos', 'que necesito']):
        if 'natural' in t or 'independiente' in t:
            return 'documentos_natural', cedula
        if 'empresa' in t or 'juridica' in t:
            return 'documentos_juridica', cedula
        return 'documentos_requeridos', cedula
    
    # Portal
    if any(p in t for p in ['portal', 'proveedores', 'registro', 'plataforma']):
        if any(p in t for p in ['problema', 'error', 'no carga', 'no funciona']):
            return 'problemas_portal', cedula
        return 'portal_proveedores', cedula
    
    # Examen médico
    if any(p in t for p in ['examen medico', 'examen ocupacional']):
        return 'examen_medico', cedula
    
    # Si no se detecta nada
    return 'general', cedula