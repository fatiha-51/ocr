from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import io

# Initialisation de l'application Flask
app = Flask(__name__)

# Chemin vers l'exécutable Tesseract (automatiquement configuré dans le conteneur)
pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"

@app.route('/ocr', methods=['POST'])
def ocr():
    try:
        # Vérifier si un fichier a été uploadé
        if 'file' not in request.files:
            return jsonify({"error": "Aucun fichier uploadé"}), 400
        
        file = request.files['file']
        
        # Vérifier si le nom du fichier est valide
        if file.filename == '':
            return jsonify({"error": "Nom de fichier invalide"}), 400
        
        # Lire l'image depuis le fichier uploadé
        img = Image.open(io.BytesIO(file.read()))
        
        # Extraire le texte avec Tesseract
        text = pytesseract.image_to_string(img)
        
        # Renvoyer le texte extrait sous forme de JSON
        return jsonify({"text": text})
    
    except Exception as e:
        # Gérer les erreurs et renvoyer un message d'erreur
        return jsonify({"error": str(e)}), 500

# Démarrer l'application Flask en mode debug (seulement pour le développement local)
if __name__ == '__main__':
    app.run(debug=True)
