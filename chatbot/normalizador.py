# chatbot/normalizador.py
"""
Normaliza el texto del usuario: limpia, convierte a minúsculas, aplica sinónimos
"""
import re
from .sinonimos import SINONIMOS

def normalizar(texto):
    """
    Normaliza el texto del usuario:
    - Convierte a minúsculas
    - Elimina caracteres especiales
    - Reemplaza sinónimos
    - Elimina espacios extra
    """
    if not texto:
        return ""
    
    # Convertir a minúsculas
    texto = texto.lower()
    
    # Eliminar caracteres especiales (mantener letras, números y algunos signos)
    texto = re.sub(r'[^\w\s\.\,\?\¿\¡]', '', texto)
    
    # Reemplazar sinónimos
    for clave, sinonimos in SINONIMOS.items():
        for sinonimo in sinonimos:
            if sinonimo in texto:
                texto = texto.replace(sinonimo, clave)
    
    # Eliminar espacios extra
    texto = re.sub(r'\s+', ' ', texto)
    
    return texto.strip()