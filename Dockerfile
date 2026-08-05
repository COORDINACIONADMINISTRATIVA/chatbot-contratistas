# Usa una imagen base de Python
FROM python:3.10-slim

# Establece el directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema (OpenCV, poppler, etc.)
RUN apt-get update && apt-get install -y \
    poppler-utils \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copia los archivos de requisitos primero (para caché de Docker)
COPY requirements.txt .

# Instala dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código
COPY . .

# Expone el puerto 5000
EXPOSE 5000

# Comando para ejecutar la app
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]