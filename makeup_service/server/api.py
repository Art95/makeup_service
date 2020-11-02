import os
import flask
import cv2
from pathlib import Path
from flask import flash, request, send_file
from werkzeug.utils import secure_filename
from makeup_service.runner import apply_makeup_on_image, apply_makeup_on_video, get_data_folder
from makeup_service.face_makeup.semantic_segmentation import SemanticSegmentation
from makeup_service.face_makeup.image_transformation import HeadPart


def get_uploads_folder_path():
    root_folder = Path(__file__).parent
    uploads_folder = os.path.join(root_folder, 'uploads')

    return uploads_folder


app = flask.Flask(__name__)
app.secret_key = os.urandom(24)

UPLOAD_FOLDER = get_uploads_folder_path()

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
        try:
            return transform_image()
        except RuntimeError as err:
            return str(err)


@app.route('/video', methods=['GET', 'POST'])
def process_video():
    if request.method == 'GET':
        return "<h1>Makeup Service</h1><p>This section is responsible for video processing.</p>"

    if request.method == 'POST':
        try:
            return transform_video()
        except RuntimeError as err:
            return str(err)


def color_string_to_list(string):
    return list(map(int, string.split(',')))


def get_file_extension(file_name):
    extension = file_name.split('.')[1]
    return extension


def allowed_file(file_name, allowed_extensions):
    extension = get_file_extension(file_name)
    return extension in allowed_extensions


def ensure_uploads_folder_exists():
    folder_path = get_uploads_folder_path()

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def get_head_parts_and_colors():
    data = request.form

    hair_color = color_string_to_list(data['hair_color'])
    upper_lip_color = color_string_to_list(data['upper_lip_color'])
    lower_lip_color = color_string_to_list(data['lower_lip_color'])

    colors = [hair_color, upper_lip_color, lower_lip_color]
    head_parts = [HeadPart.hair, HeadPart.upper_lip, HeadPart.lower_lip]

    return head_parts, colors


def save_data_source_to_file(allowed_extensions):
    data_key = 'source'

    if data_key not in request.files:
        flash('No file part')
        raise RuntimeError("No file was provided")

    source = request.files[data_key]

    if source.filename == '':
        flash('No selected file')
        raise RuntimeError("File was not selected")

    if not source or not allowed_file(source.filename, allowed_extensions):
        flash('Invalid file')
        raise RuntimeError("Invalid file")

    ensure_uploads_folder_exists()

    file_name = secure_filename(source.filename)
    full_file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    source.save(full_file_path)

    return file_name


def transform_image():
    allowed_extensions = {'png', 'jpg', 'jpeg'}
    head_parts, colors = get_head_parts_and_colors()

    file_name = save_data_source_to_file(allowed_extensions)
    full_image_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)

    image_orig = cv2.imread(full_image_path)
    transformed_image = apply_makeup_on_image(image_orig, segmentation_model, head_parts, colors)

    transformed_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'transformed_' + file_name)

    cv2.imwrite(transformed_file_path, transformed_image)

    extension = get_file_extension(file_name)

    return send_file(transformed_file_path, mimetype='image/' + extension)


def transform_video():
    allowed_extensions = {'avi'}
    head_parts, colors = get_head_parts_and_colors()

    file_name = save_data_source_to_file(allowed_extensions)
    full_video_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    transformed_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'transformed_' + file_name)

    apply_makeup_on_video(full_video_path, colors, save_to_file=True, out_file_path=transformed_file_path)

    extension = get_file_extension(file_name)

    return send_file(transformed_file_path, mimetype='video/' + extension)


app.run(debug=True)
