# chatbot/sinonimos.py
"""
Diccionario de sinónimos para normalizar el texto del usuario
"""

SINONIMOS = {
    # Verbos de acción
    'subir': ['subir', 'mandar', 'enviar', 'cargar', 'adjuntar', 'poner', 'agregar', 'entregar', 'montar', 'colocar'],
    'registrar': ['registrar', 'inscribir', 'matricular', 'anotar', 'apuntar', 'crear', 'inscribirme', 'registrarme'],
    'actualizar': ['actualizar', 'renovar', 'cambiar', 'modificar', 'arreglar', 'corregir', 'sacar nuevo', 'renovarlo'],
    'validar': ['validar', 'verificar', 'revisar', 'analizar', 'chequear', 'confirmar', 'checar'],
    'consultar': ['consultar', 'preguntar', 'averiguar', 'saber', 'conocer', 'ver', 'mirar'],
    
    # Sustantivos clave
    'rut': ['rut', 'RUT', 'r.u.t', 'R.U.T', 'ese documento', 'el rut ese', 'rut ese', 'registro unico tributario'],
    'documentos': ['documentos', 'papeles', 'papelería', 'requisitos', 'anexos', 'archivos', 'formatos', 'documentación'],
    'portal': ['portal', 'plataforma', 'sistema', 'página', 'sitio', 'aplicación', 'programa', 'proveedores'],
    'registro': ['registro', 'inscripción', 'matrícula', 'creación de cuenta', 'alta', 'inscripcion'],
    'sede': ['sede', 'oficina', 'ubicación', 'lugar', 'dirección', 'rectoría'],
    'regimen': ['regimen', 'régimen', 'tipo de contribuyente', 'régimen tributario', 'regimen tributario'],
    'tratamiento': ['tratamiento', 'título', 'forma de trato', 'señor o señora'],
    'codigo postal': ['código postal', 'codigo postal', 'código', 'zip code', 'codigo de área'],
    
    # Errores comunes
    'reguimen': 'regimen',
    'sertificacion': 'certificacion',
    'cotisacion': 'cotizacion',
    'sedee': 'sede',
    'rtu': 'rut',
    'probeedores': 'proveedores',
    'inscripcion': 'registro',
    
    # Coloquialismos
    'pa': 'para',
    'pq': 'porque',
    'xq': 'porque',
    'bn': 'bien',
    'toy': 'estoy',
    'xfa': 'por favor',
    'q': 'que',
}