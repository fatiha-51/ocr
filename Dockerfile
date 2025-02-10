# Dockerfile
FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y tesseract-ocr poppler-utils libgl1 tesseract-ocr-fra tesseract-ocr-spa && \
    apt-get clean

WORKDIR /app
COPY requirements.txt app.py .  # <-- Ne copiez QUE app.py, pas main.py

RUN pip install --no-cache-dir -r requirements.txt

CMD gunicorn --bind 0.0.0.0:${PORT:-8000} --timeout 120 app:app  # <-- app:app (pas main)
