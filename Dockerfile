FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    libgl1 \
    tesseract-ocr-fra \
    tesseract-ocr-spa && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt app.py .

RUN pip install --no-cache-dir -r requirements.txt

CMD gunicorn --bind 0.0.0.0:${PORT:-8000} --workers=4 --timeout 120 app:app
