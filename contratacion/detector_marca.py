# backend/contratacion/detector_marca.py
"""
Detector de marca de agua en RUTs usando PCA (Análisis de Componentes Principales).
Distingue sello VÁLIDO (círculo) de INVÁLIDO (diagonal).
"""
import os
import cv2
import numpy as np
from pdf2image import convert_from_path
from config import POPPLER_PATH  # <--- IMPORTAR LA RUTA

# ============================================================
# CONFIGURACIÓN (calibrada con RUTs reales)
# ============================================================
DPI = 350

# Rango de gris de la tinta del sello (medido por histograma)
GRIS_MIN = 155
GRIS_MAX = 195

# Región donde vive el sello dentro de la página (x, y, ancho, alto)
# Calibrado sobre RUTs en tamaño carta a 350 DPI (página 3850x2975 px)
BBOX_SELLO = (146, 700, 2474, 2201)

# Umbrales de la razón PCA
UMBRAL_VALIDO = 6.0
UMBRAL_INVALIDO = 4.5

# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def analizar_marca_agua_por_pca(ruta_pdf, poppler_path=None):
    """
    Analiza la marca de agua de un RUT en PDF usando PCA.
    Retorna un diccionario con el estado y el ratio_pca.
    """
    try:
        # Convertir PDF a imagen
        poppler_path = POPPLER_PATH
        paginas = convert_from_path(ruta_pdf, dpi=DPI, poppler_path=poppler_path)
        img_pil = paginas[0]
        img_bgr = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

        # Convertir a gris
        gris = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        x, y, w, h = BBOX_SELLO
        recorte = gris[y:y+h, x:x+w]

        # Máscara para el rango de gris del sello
        mascara = cv2.inRange(recorte, GRIS_MIN, GRIS_MAX)
        ys, xs = np.nonzero(mascara)

        if len(xs) < 500:
            return {"estado": "sin_marca", "ratio_pca": None, "n_pixeles": len(xs)}

        # PCA sobre las coordenadas de los píxeles de tinta
        puntos = np.column_stack([xs, ys]).astype(np.float64)
        puntos_centrados = puntos - puntos.mean(axis=0)
        cov = np.cov(puntos_centrados.T)
        valores = sorted(np.linalg.eigh(cov)[0], reverse=True)
        ratio = valores[0] / valores[1] if valores[1] > 0 else 999

        # Clasificar según los umbrales
        if ratio >= UMBRAL_VALIDO:
            estado = "valido"
        elif ratio <= UMBRAL_INVALIDO:
            estado = "invalido"
        else:
            estado = "revisar_manual"

        return {"estado": estado, "ratio_pca": round(ratio, 3), "n_pixeles": len(xs)}

    except Exception as e:
        return {"estado": "error", "error": str(e)}