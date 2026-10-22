import os
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from pdf2docx import Converter

app = Flask(__name__)
CORS(app)  # Is se WordPress website humari API se connect ho sakti hai

UPLOAD_FOLDER = "uploads"
CONVERTED_FOLDER = "converted"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

@app.route('/convert', methods=['POST'])
def convert_pdf_to_word():
    if 'pdf_file' not in request.files:
        return jsonify({"error": "PDF file upload nahi hui"}), 400

    file = request.files['pdf_file']
    if file.filename == '':
        return jsonify({"error": "Koi file select nahi ki gayi"}), 400

    if file:
        pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
        docx_filename = os.path.splitext(file.filename)[0] + ".docx"
        docx_path = os.path.join(CONVERTED_FOLDER, docx_filename)

        # File save karein
        file.save(pdf_path)

        try:
            # PDF ko Word mein convert karein
            cv = Converter(pdf_path)
            cv.convert(docx_path, start=0, end=None)
            cv.close()

            # Converted file user ko download ke liye bhejein
            return send_file(docx_path, as_attachment=True)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)