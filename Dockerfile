# Base image
FROM python:3.9-slim

# Mettre à jour les paquets et installer Tesseract
RUN apt-get update && \
    apt-get install -y tesseract-ocr && \
    apt-get install -y poppler-utils && \
    apt-get install -y libtesseract-dev && \
    apt-get clean

# Installer les langues supplémentaires pour Tesseract (facultatif)
RUN apt-get install -y tesseract-ocr-fra tesseract-ocr-spa

# Créer un répertoire pour l'application
WORKDIR /app

# Copier les fichiers du projet
COPY . .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port 8000 (par défaut utilisé par Render)
EXPOSE 8000

# Démarrer l'application avec Gunicorn
CMD ["gunicorn", "--workers=3", "--bind", ":8000", "app:app"]
