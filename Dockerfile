FROM python:3.12-slim

WORKDIR /app

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    poppler-utils \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ⚠️ Asegura que gunicorn esté instalado
RUN pip install gunicorn

COPY . .

EXPOSE 5000

# El CMD se ejecutará si el Start Command está vacío
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--workers=1", "--threads=2"]