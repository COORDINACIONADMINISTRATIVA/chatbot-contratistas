from config import TESSERACT_PATH, POPPLER_PATH

import pytesseract
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def leer_pdf_ocr(ruta_pdf):

    paginas = convert_from_path(
        ruta_pdf,
        poppler_path=POPPLER_PATH
    )

    texto = ""

    for pagina in paginas:
        texto += pytesseract.image_to_string(
            pagina,
            lang="spa"
        )

    texto = texto.strip()

    return texto if texto else None