# Base image
FROM python:3.9-slim

# Installer les dépendances système
RUN apt-get update && \
    apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    libgl1 \
    tesseract-ocr-fra \
    tesseract-ocr-spa && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Créer le répertoire de l'application
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt .
COPY app.py .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port (utilisé par Render)
EXPOSE $PORT

# Commande de démarrage avec variable d'environnement Render
CMD gunicorn --workers=3 --bind 0.0.0.0:${PORT:-8000} --timeout 120 app:app
