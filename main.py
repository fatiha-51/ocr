# main.py

from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import io

app = Flask(__name__)

pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"

@app.route('/ocr', methods=['POST'])
def ocr():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "Aucun fichier uploadé"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "Nom de fichier invalide"}), 400
        
        img = Image.open(io.BytesIO(file.read()))
        text = pytesseract.image_to_string(img)
        
        return jsonify({"text": text})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
