import os
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from csv_converter import csv_to_json

UPLOAD_FOLDER = r'C:\Users\rohan\AppData\Local\Programs\Python\Python37-32\My programs\api'
ALLOWED_EXTENSIONS = ['csv']
OUTPUT_FILENAME = 'data.json'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

op_path = os.path.join(app.config['UPLOAD_FOLDER'], OUTPUT_FILENAME)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def hello() -> str:
    resp = jsonify({'message': 'Welcome to the Json builder. Upload your CSV file at URL /upload-file'})
    resp.status_code = 200
    return resp


@app.route('/upload-file', methods=['POST'])
def upload_file() -> None:
    if 'file' not in request.files:
        resp = jsonify({'message': 'File missing in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        ip_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(ip_path)
        csv_to_json(ip_path, op_path)
        resp = jsonify({'message': 'File successfully uploaded. Converted JSON can be found at URL /converted-json'})
        resp.status_code = 200
        return resp
    else:
        resp = jsonify({'message': 'Only CSV files are allowed'})
        resp.status_code = 400
        return resp


@app.route('/converted-json')
def return_json() -> None:
    if os.path.exists(op_path):
        return send_from_directory(app.config['UPLOAD_FOLDER'],
                                   OUTPUT_FILENAME,
                                   as_attachment=True
                                   )
    else:
        resp = jsonify({'message': 'JSON not available. To generate JSON upload CSV at URL /upload-file'})
        resp.status_code = 400
        return resp


if __name__ == '__main__':
    app.run()
