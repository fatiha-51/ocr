from flask import Flask, request, jsonify
import pytesseract
from PIL import Image, UnidentifiedImageError
import io
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/ocr', methods=['POST'])
def ocr():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "Aucun fichier uploadé"}), 400

        file = request.files['file']
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({"error": "Nom de fichier invalide ou extension non autorisée"}), 400

        try:
            img = Image.open(io.BytesIO(file.read()))
        except UnidentifiedImageError:
            return jsonify({"error": "Fichier non valide ou non reconnu comme une image"}), 400

        text = pytesseract.image_to_string(img)
        return jsonify({"text": text})

    except Exception as e:
        logging.error(f"Erreur lors de l'OCR: {str(e)}")
        return jsonify({"error": "Une erreur est survenue lors du traitement de l'image"}), 500

# Suppression totale du bloc if __name__ == '__main__'
