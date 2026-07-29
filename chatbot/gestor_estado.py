# chatbot/gestor_estado.py
"""
Gestor de estado conversacional para flujos guiados
Cada usuario tiene: flujo_actual, paso_actual, datos_recolectados
"""

from collections import defaultdict

class GestorEstado:
    def __init__(self):
        # Estado por usuario: { 'flujo': 'registro', 'paso': 0, 'datos': {}, 'historial': [] }
        self.estados = defaultdict(lambda: {
            'flujo': None,       # Nombre del flujo actual (ej: 'registro')
            'paso': 0,           # Índice del paso actual (0 = primer paso)
            'datos': {},         # Datos recolectados durante el flujo
            'historial': [],     # Historial de interacciones
            'ultimo_tema': None  # Último tema consultado (para contexto)
        })
        print(f"🆔 Instancia de GestorEstado creada con ID: {id(self)}")
    
    def obtener_estado(self, usuario):
        """Obtiene el estado de un usuario"""
        return self.estados[usuario]
    
    def iniciar_flujo(self, usuario, flujo_id):
        """Inicia un nuevo flujo para el usuario"""
        estado = self.estados[usuario]
        estado['flujo'] = flujo_id
        estado['paso'] = 0
        estado['datos'] = {}
        estado['historial'] = []
        estado['ultimo_tema'] = flujo_id
        return estado
    
    def avanzar_paso(self, usuario):
        """Avanza al siguiente paso del flujo"""
        estado = self.estados[usuario]
        estado['paso'] += 1
        return estado
    
    def retroceder_paso(self, usuario):
        """Retrocede al paso anterior del flujo"""
        estado = self.estados[usuario]
        if estado['paso'] > 0:
            estado['paso'] -= 1
        return estado
    
    def guardar_dato(self, usuario, clave, valor):
        """Guarda un dato recolectado durante el flujo"""
        estado = self.estados[usuario]
        estado['datos'][clave] = valor
        return estado
    
    def obtener_dato(self, usuario, clave, default=None):
        """Obtiene un dato recolectado"""
        estado = self.estados[usuario]
        return estado['datos'].get(clave, default)
    
    def obtener_paso_actual(self, usuario):
        """Obtiene el paso actual del flujo"""
        estado = self.estados[usuario]
        return estado['paso']
    
    def obtener_flujo_actual(self, usuario):
        """Obtiene el flujo actual"""
        estado = self.estados[usuario]
        return estado['flujo']
    
    def esta_en_flujo(self, usuario):
        """Verifica si el usuario está en medio de un flujo"""
        estado = self.estados[usuario]
        return estado['flujo'] is not None
    
    def resetear(self, usuario):
        """Resetea el estado del usuario (vuelve al menú principal)"""
        estado = self.estados[usuario]
        estado['flujo'] = None
        estado['paso'] = 0
        estado['datos'] = {}
        estado['historial'] = []
        return estado
    
    def agregar_historial(self, usuario, mensaje, rol='usuario'):
        """Agrega un mensaje al historial"""
        estado = self.estados[usuario]
        estado['historial'].append({
            'rol': rol,
            'mensaje': mensaje,
            'timestamp': __import__('datetime').datetime.now().isoformat()
        })
        # Mantener solo los últimos 20 mensajes
        if len(estado['historial']) > 20:
            estado['historial'] = estado['historial'][-20:]
# chatbot/gestor_estado.py (agregar este método dentro de la clase GestorEstado)
    def ir_a_paso(self, usuario, paso):
        """Establece el paso actual del flujo."""
        estado = self.estados[usuario]
        estado['paso'] = paso
        return estado
    
    def ir_a_paso(self, usuario, paso):
        """Establece el paso actual del flujo."""
        estado = self.estados[usuario]
        estado['paso'] = paso
        return estado
# Instancia global
gestor = GestorEstado()

