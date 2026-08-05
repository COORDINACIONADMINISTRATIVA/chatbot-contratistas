FROM python:3.10-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-spa \
    poppler-utils \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Configurar variables de entorno para Tesseract y Poppler
ENV TESSERACT_PATH=/usr/bin/tesseract
ENV POPPLER_PATH=/usr/bin

WORKDIR /app

COPY requirements.txt .

# Instalar torch sin CUDA (necesario para sentence-transformers)
RUN pip install torch==2.0.1 --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p uploads

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "app:app"]