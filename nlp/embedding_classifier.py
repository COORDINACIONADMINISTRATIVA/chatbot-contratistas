"""
Clasificador de intenciones usando EMBEDDINGS SEMÁNTICOS
Entiende el SIGNIFICADO de las preguntas, no solo palabras exactas
"""
import json
import os
import random
import numpy as np
from sentence_transformers import SentenceTransformer, util
import joblib


class EmbeddingClassifier:
    """
    Clasificador de intenciones por similitud semántica (embeddings).
    Es genérico: recibe qué base de conocimiento usar y dónde guardar los
    embeddings entrenados, para poder tener varios "bots" sin que se pisen
    los archivos entre sí.
    """

    def __init__(self, faqs_filename='faqs_contratista.json', prefix='contratista'):
        self.model_name = 'paraphrase-multilingual-MiniLM-L12-v2'
        self.model = None
        self.intent_embeddings = None
        self.intent_data = []
        self.responses = {}
        self.faqs_filename = faqs_filename
        models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
        self.embeddings_path = os.path.join(models_dir, f'{prefix}_intent_embeddings.npz')
        self.meta_path = os.path.join(models_dir, f'{prefix}_embedding_meta.json')

    def cargar_base_conocimiento(self):
        ruta = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'knowledge_base', self.faqs_filename
        )
        with open(ruta, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data['intents']
    
    def cargar_modelo(self):
        """Carga el modelo de embeddings"""
        print(f"Cargando modelo de embeddings ({self.model_name})...")
        self.model = SentenceTransformer(self.model_name)
        
        if os.path.exists(self.embeddings_path):
            print("Cargando embeddings pre-calculados...")
            data = np.load(self.embeddings_path, allow_pickle=True)
            self.intent_embeddings = data['embeddings']
            with open(self.meta_path, 'r', encoding='utf-8') as f:
                meta = json.load(f)
            self.intent_data = meta['intent_data']
            self.responses = meta['responses']
            print(f"Cargados {len(self.intent_data)} patrones")
        else:
            print("No hay embeddings guardados, entrenando...")
            self.entrenar()
    
    def entrenar(self):
        """Calcula los embeddings de todos los patrones"""
        intents = self.cargar_base_conocimiento()
        
        self.intent_data = []
        self.responses = {}
        
        for intent in intents:
            tag = intent['tag']
            self.responses[tag] = intent.get('respuestas', ['No tengo respuesta.'])
            
            for patron in intent.get('patrones', []):
                if patron and patron.strip():
                    self.intent_data.append({
                        'texto': patron,
                        'tag': tag
                    })
        
        print(f"Calculando embeddings para {len(self.intent_data)} patrones...")
        textos = [d['texto'] for d in self.intent_data]
        self.intent_embeddings = self.model.encode(textos, convert_to_numpy=True)
        
        os.makedirs(os.path.dirname(self.embeddings_path), exist_ok=True)
        np.savez(self.embeddings_path, embeddings=self.intent_embeddings)
        with open(self.meta_path, 'w', encoding='utf-8') as f:
            json.dump({
                'intent_data': self.intent_data,
                'responses': self.responses
            }, f, ensure_ascii=False)
        
        print(f"Entrenamiento completo: {len(self.intent_data)} patrones indexados")
    
    def predecir(self, texto, umbral=0.40):
        """
        Predice la intención por SIMILITUD SEMÁNTICA
        """
        texto_limpio = texto.lower().strip()
        embedding_usuario = self.model.encode([texto_limpio], convert_to_numpy=True)[0]
        similitudes = util.cos_sim(embedding_usuario, self.intent_embeddings)[0]
        
        idx_max = int(np.argmax(similitudes))
        similitud = float(similitudes[idx_max])
        intencion = self.intent_data[idx_max]['tag']
        
        if similitud < umbral:
            return 'fuera_de_alcance', similitud
        
        return intencion, similitud
    
    def obtener_respuesta(self, intencion):
        if intencion in self.responses and self.responses[intencion]:
            return random.choice(self.responses[intencion])
        return "No tengo informacion sobre eso."


if __name__ == '__main__':
    # Para (re)entrenar el modelo del CONTRATISTA de verdad, corre:
    #   python models/entrenar_modelo.py
    print("Usa 'python models/entrenar_modelo.py' para entrenar/probar el clasificador.")