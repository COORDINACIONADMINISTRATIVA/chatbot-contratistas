FROM python:3.11-slim

WORKDIR /app

# Instala dependencias del sistema (las necesarias para OpenCV, poppler, numpy, etc.)
RUN apt-get update && apt-get install -y \
    poppler-utils \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgcc-s1 \
    libstdc++6 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Comando de inicio
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--workers=1", "--threads=2"]