"""
Entrena el clasificador semántico (embeddings) del chatbot de CONTRATISTAS.

Qué hace "entrenar" aquí en la práctica:
No es una red neuronal que se entrena desde cero. Usamos un modelo de
lenguaje ya entrenado (sentence-transformers, 'paraphrase-multilingual-MiniLM-L12-v2')
que sabe medir qué tan parecidas son dos frases EN SIGNIFICADO. "Entrenar"
consiste en calcularle a ese modelo el embedding (vector numérico) de cada
frase de ejemplo en knowledge_base/faqs_contratista.json, y guardar esos
vectores en disco (models/contratista_intent_embeddings.npz). Así, cuando
llega un mensaje nuevo del usuario, solo hay que compararlo contra esos
vectores ya calculados (rápido) en vez de recalcular todo cada vez.

Uso:
    python models/entrenar_modelo.py             -> entrena y prueba
    python models/entrenar_modelo.py --solo-entrenar
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nlp.embedding_classifier import EmbeddingClassifier

# Casos de prueba: (frase del usuario, intención esperada)
PRUEBAS = [
    ("hola", "saludo"),
    ("buenas tardes", "saludo"),
    ("quiero subir mi rut", "subir_rut"),
    ("me ayudas a revisar el rut", "subir_rut"),
    ("cada cuanto toca actualizar el rut", "actualizar_rut"),
    ("donde me registro como proveedor", "portal_proveedores"),
    ("que documentos necesito si soy independiente", "documentos_natural"),
    ("documentos si somos una empresa", "documentos_juridica"),
    ("que necesito para el contrato", "documentos_requeridos"),
    ("no se que poner en el campo de sede", "llenar_plataforma"),
    ("se rechazo mi registro en el portal", "problemas_registro"),
    ("ya me pagaron la factura", "estado_pago"),
    ("cuentame un chiste", "fuera_de_alcance"),
]


def entrenar():
    print("=" * 60)
    print("ENTRENANDO CLASIFICADOR DEL CHATBOT DE CONTRATISTAS")
    print("=" * 60)
    clf = EmbeddingClassifier()
    print(f"Cargando modelo base: {clf.model_name} ...")
    from sentence_transformers import SentenceTransformer
    clf.model = SentenceTransformer(clf.model_name)
    clf.entrenar()
    print(f"Guardado en: {clf.embeddings_path}")
    print(f"Metadatos en: {clf.meta_path}")
    return clf


def probar(clf=None):
    if clf is None:
        clf = EmbeddingClassifier()
        clf.cargar_modelo()

    print("\n" + "=" * 60)
    print("PRUEBAS DE PRECISIÓN")
    print("=" * 60)
    aciertos = 0
    for texto, esperado in PRUEBAS:
        intencion, similitud = clf.predecir(texto)
        ok = "OK  " if intencion == esperado else "FAIL"
        if intencion == esperado:
            aciertos += 1
        print(f"[{ok}] '{texto}' -> {intencion} ({similitud:.0%}) [esperado: {esperado}]")

    total = len(PRUEBAS)
    print(f"\nPrecisión: {aciertos}/{total} = {aciertos / total * 100:.0f}%")


if __name__ == '__main__':
    clf = entrenar()
    if '--solo-entrenar' not in sys.argv:
        probar(clf)
