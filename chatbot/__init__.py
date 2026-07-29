# chatbot/__init__.py
from .motor import responder
from .memoria import memoria
from .gestor_estado import gestor
from .respuestas import RESPUESTAS
from .respuestas_campos import RESPUESTAS_CAMPOS

__all__ = ['responder', 'memoria', 'gestor', 'RESPUESTAS', 'RESPUESTAS_CAMPOS']