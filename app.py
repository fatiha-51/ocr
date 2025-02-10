from flask import Flask, request, jsonify
import pytesseract
from PIL import Image, UnidentifiedImageError
import io
import logging

# Initialisation de l'application Flask
app = Flask(__name__)

# Configuration du logging
logging.basicConfig(level=logging.INFO)

# Chemin vers l'exécutable Tesseract (automatiquement configuré dans le conteneur)
pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"

# Liste des extensions de fichiers autorisées
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}

def allowed_file(filename):
    """Vérifie si le fichier a une extension autorisée."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/ocr', methods=['POST'])
def ocr():
    try:
        # Vérifier si un fichier a été uploadé
        if 'file' not in request.files:
            return jsonify({"error": "Aucun fichier uploadé"}), 400

        file = request.files['file']

        # Vérifier si le nom du fichier est valide et autorisé
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({"error": "Nom de fichier invalide ou extension non autorisée"}), 400

        # Lire l'image depuis le fichier uploadé
        try:
            img = Image.open(io.BytesIO(file.read()))
        except UnidentifiedImageError:
            return jsonify({"error": "Fichier non valide ou non reconnu comme une image"}), 400

        # Extraire le texte avec Tesseract
        text = pytesseract.image_to_string(img)

        # Renvoyer le texte extrait sous forme de JSON
        return jsonify({"text": text})

    except Exception as e:
        # Gérer les erreurs et renvoyer un message d'erreur
        logging.error(f"Erreur lors de l'OCR: {str(e)}")
        return jsonify({"error": "Une erreur est survenue lors du traitement de l'image"}), 500

# Démarrer l'application Flask en mode debug (seulement pour le développement local)
if __name__ == '__main__':
    app.run(debug=True)
