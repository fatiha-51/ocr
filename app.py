# app.py

from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import io

app = Flask(__name__)

# Chemin vers l'exécutable Tesseract (automatiquement configuré dans le conteneur)
pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"

@app.route('/ocr', methods=['POST'])
def ocr():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "Aucun fichier uploadé"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "Nom de fichier invalide"}), 400
        
        # Lire l'image depuis le fichier uploadé
        img = Image.open(io.BytesIO(file.read()))
        
        # Extraire le texte avec Tesseract
        text = pytesseract.image_to_string(img)
        
        return jsonify({"text": text})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
