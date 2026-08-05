import os
TESSERACT_PATH = os.environ.get("TESSERACT_PATH", "tesseract")
POPPLER_PATH = os.environ.get("POPPLER_PATH", None)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POPPLER_PATH = r"C:\poppler\Library\bin"  # <--- EJEMPLO EN WINDOWS
