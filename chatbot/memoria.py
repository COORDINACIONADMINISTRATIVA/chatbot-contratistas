# chatbot/memoria.py
"""
Sistema de memoria conversacional para el chatbot
Guarda el contexto de la conversación de cada usuario
"""
from collections import defaultdict
from datetime import datetime

class MemoriaConversacional:
    def __init__(self):
        # Historial de mensajes por usuario
        self.historial = defaultdict(list)
        # Contexto actual por usuario
        self.contexto = defaultdict(dict)
        # Última intención por usuario
        self.ultima_intencion = defaultdict(str)
        # Última pregunta del usuario por usuario
        self.ultima_pregunta = defaultdict(str)
        # Última respuesta del bot por usuario
        self.ultima_respuesta = defaultdict(str)
        # Última cédula consultada por usuario
        self.ultima_cedula = defaultdict(str)
    
    def guardar_mensaje(self, usuario, mensaje, tipo="usuario", intencion=None, cedula=None):
        """Guarda un mensaje en el historial del usuario"""
        self.historial[usuario].append({
            'tipo': tipo,
            'mensaje': mensaje,
            'intencion': intencion,
            'cedula': cedula,
            'timestamp': datetime.now().isoformat()
        })
        # Guardar solo los últimos 50 mensajes
        if len(self.historial[usuario]) > 50:
            self.historial[usuario] = self.historial[usuario][-50:]
        
        # Si es mensaje del usuario, guardar como última pregunta
        if tipo == "usuario":
            self.ultima_pregunta[usuario] = mensaje
        # Si es respuesta del bot, guardar como última respuesta
        elif tipo == "bot":
            self.ultima_respuesta[usuario] = mensaje
    
    def guardar_contexto(self, usuario, clave, valor):
        """Guarda una variable de contexto para el usuario"""
        self.contexto[usuario][clave] = valor
    
    def obtener_contexto(self, usuario, clave, default=None):
        """Obtiene una variable de contexto del usuario"""
        return self.contexto[usuario].get(clave, default)
    
    def guardar_intencion(self, usuario, intencion):
        """Guarda la última intención del usuario"""
        self.ultima_intencion[usuario] = intencion
    
    def obtener_ultima_intencion(self, usuario):
        """Obtiene la última intención del usuario"""
        return self.ultima_intencion.get(usuario, None)
    
    def obtener_ultima_pregunta(self, usuario):
        """Obtiene la última pregunta del usuario"""
        return self.ultima_pregunta.get(usuario, None)
    
    def obtener_ultima_respuesta(self, usuario):
        """Obtiene la última respuesta del bot"""
        return self.ultima_respuesta.get(usuario, None)
    
    def guardar_cedula(self, usuario, cedula):
        """Guarda la última cédula consultada por el usuario"""
        self.ultima_cedula[usuario] = cedula
    
    def obtener_ultima_cedula(self, usuario):
        """Obtiene la última cédula consultada por el usuario"""
        return self.ultima_cedula.get(usuario, None)
    
    def obtener_tema_actual(self, usuario):
        """Obtiene el tema actual de la conversación"""
        return self.contexto[usuario].get('tema', None)
    
    def esta_hablando_de(self, usuario, tema):
        """Verifica si el usuario está hablando de un tema específico"""
        return self.contexto[usuario].get('tema') == tema
    
    def limpiar(self, usuario):
        """Limpia el contexto de un usuario"""
        if usuario in self.contexto:
            self.contexto[usuario] = {}
        if usuario in self.ultima_intencion:
            self.ultima_intencion[usuario] = None
        if usuario in self.ultima_cedula:
            self.ultima_cedula[usuario] = None
        if usuario in self.ultima_pregunta:
            self.ultima_pregunta[usuario] = None
        if usuario in self.ultima_respuesta:
            self.ultima_respuesta[usuario] = None

# Instancia global
memoria = MemoriaConversacional()