FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    poppler-utils \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# El CMD se ejecutará si el Start Command está vacío
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]

RUN pip install gunicorn