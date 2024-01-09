import base64

import torch
from flask import Flask, request, jsonify, send_file
import os
import time
from languageClass import classify_audio
from Dataset import generate_random_story_prompt
from TTS import TTS_input
from ImageGeneration import getImage

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav'}  # Allowed audio file extensions

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def detect_country(path):
    print("detecting country")
    country = classify_audio(path)
    return country


def generate_story(country):
    if country == 'other':
        return None
    print("generating story")
    story, prompt = generate_random_story_prompt(country)
    TTS_input(story)
    getImage(prompt)



@app.route('/image', methods=["GET"])
def return_image():
    country_name = request.args.get('country_name', default='India')
    print(country_name)
    generate_story(country_name)
    local_path = 'imageDemo.png'
    with open(local_path, 'rb') as f:
        image_data = f.read()

    # Encode the image bytes to base64
    encoded_image = base64.b64encode(image_data).decode('utf-8')

    return {
        'image': encoded_image,
        'mime_type': 'image.png'  # Adjust the MIME type based on your image format
    }


@app.route('/story', methods=["GET"])
def return_audio():
    print("returning audio")
    audio_file_path = "output_audio.wav"  # Replace with your actual file path
    return send_file(audio_file_path, as_attachment=True)


def allowed_file(filename):
    print("checking file")
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# first route "empty route"
@app.route('/', methods=["GET"])
def index():
    print("first route")
    return "first route"


@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    print("uploading audio")
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        # Save the uploaded file
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        detected_language = detect_country(filepath)
        # Use the detected language information in the response
        return jsonify({'message': 'File successfully uploaded and saved', 'detected_country': detected_language}), 200

    return jsonify({'error': 'Invalid file format'}), 400


if __name__ == '__main__':
    app.run(debug=True, port=2333)
