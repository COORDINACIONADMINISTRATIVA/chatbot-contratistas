try:
    from pypdf import PdfReader
except ImportError:
    from PyPDF2 import PdfReader


def leer_pdf(ruta_pdf):
    """
    Intenta leer un PDF digital.
    Si no encuentra texto, usa OCR automáticamente.
    """

    try:
        reader = PdfReader(ruta_pdf)

        texto = ""

        for pagina in reader.pages:
            contenido = pagina.extract_text()

            if contenido:
                texto += contenido + "\n"

        texto = texto.strip()

        if texto:
            print("✅ PDF digital detectado")
            return texto

        print("📄 PDF sin texto. Intentando OCR...")

    except Exception as e:
        print(f"Error leyendo PDF: {e}")

    # Solo importamos OCR cuando realmente se necesita
    try:
        from contratacion.lector_ocr import leer_pdf_ocr

        return leer_pdf_ocr(ruta_pdf)

    except Exception as e:
        print(f"Error usando OCR: {e}")
        return None