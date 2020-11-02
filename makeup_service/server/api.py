import os
import flask
import cv2
from pathlib import Path
from flask import flash, request, redirect, send_file
from werkzeug.utils import secure_filename
from makeup_service.runner import apply_makeup_on_image, get_data_folder
from makeup_service.face_makeup.semantic_segmentation import SemanticSegmentation
from makeup_service.face_makeup.image_transformation import HeadPart


def get_uploads_folder_path():
    root_folder = Path(__file__).parent
    uploads_folder = os.path.join(root_folder, 'uploads')

    return uploads_folder


app = flask.Flask(__name__)
UPLOAD_FOLDER = get_uploads_folder_path()
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model_path = os.path.join(get_data_folder(), 'bisenet_model.pth')
segmentation_model = SemanticSegmentation(model_path)


@app.route('/', methods=['GET'])
def home():
    return "<h1>Makeup Service</h1><p>This site is a prototype API for makeup service application.</p>"


@app.route('/image', methods=['GET', 'POST'])
def process_image():
    if request.method == 'GET':
        return "<h1>Makeup Service</h1><p>This section is responsible for image processing.</p>"

    if request.method == 'POST':
        data = request.form

        hair_color = color_string_to_list(data['hair_color'])
        upper_lip_color = color_string_to_list(data['upper_lip_color'])
        lower_lip_color = color_string_to_list(data['lower_lip_color'])

        colors = [hair_color, upper_lip_color, lower_lip_color]
        head_parts = [HeadPart.hair, HeadPart.upper_lip, HeadPart.lower_lip]

        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)

        image = request.files['image']

        if image.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if image and allowed_file(image.filename):
            ensure_uploads_folder_exists()

            file_name = secure_filename(image.filename)
            full_file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            image.save(full_file_path)

            image_orig = cv2.imread(full_file_path)
            transformed_image = apply_makeup_on_image(image_orig, segmentation_model, head_parts, colors)

            transformed_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'transformed_' + file_name)

            cv2.imwrite(transformed_file_path, transformed_image)

            extension = get_file_extension(file_name)

            return send_file(transformed_file_path, mimetype='image/' + extension)

        return "Fail"


@app.route('/video', methods=['GET'])
def process_video():
    return "<h1>Makeup Service</h1><p>This section is responsible for video processing.</p>"


def color_string_to_list(string):
    return list(map(int, string.split(',')))


def get_file_extension(file_name):
    extension = file_name.split('.')[1]
    return extension


def allowed_file(file_name):
    extension = get_file_extension(file_name)
    return extension in ALLOWED_EXTENSIONS


def ensure_uploads_folder_exists():
    folder_path = get_uploads_folder_path()

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


app.run(debug=True)
