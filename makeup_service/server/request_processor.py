import cv2
import io
import os
import numpy as np
from flask import flash, send_file
from werkzeug.utils import secure_filename
from makeup_service.server.face_makeup_facade import FaceMakeupFacade
from makeup_service.server.common import get_uploads_folder_path

face_makeup = FaceMakeupFacade()


def transform_image(request):
    allowed_extensions = {'png', 'jpg', 'jpeg'}
    colors = get_colors(request)

    image, file_name = get_image_from_request(request, allowed_extensions)
    transformed_image = face_makeup.apply_makeup_on_image(image, colors)

    extension = get_file_extension(file_name)

    retval, buffer = cv2.imencode("." + extension, transformed_image)

    return send_file(io.BytesIO(buffer), mimetype='image/' + extension)


def transform_video(request):
    allowed_extensions = {'avi'}
    colors = get_colors(request)

    file_name = get_video_file_from_request(request, allowed_extensions)
    video_file_full_path = os.path.join(get_uploads_folder_path(), file_name)
    transformed_file_path = os.path.join(get_uploads_folder_path(), 'transformed_' + file_name)

    face_makeup.apply_makeup_on_video(video_file_full_path, colors, save_to_file=True,
                                      out_file_path=transformed_file_path)

    extension = get_file_extension(file_name)

    return send_file(transformed_file_path, mimetype='video/' + extension)


def color_string_to_list(string):
    return list(map(int, string.split(',')))


def get_file_extension(file_name):
    extension = file_name.split('.')[1]
    return extension


def is_allowed_file(file_name, allowed_extensions):
    extension = get_file_extension(file_name)
    return extension in allowed_extensions


def ensure_uploads_folder_exists():
    folder_path = get_uploads_folder_path()

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def get_colors(request):
    data = request.form

    hair_color = color_string_to_list(data['hair_color'])
    upper_lip_color = color_string_to_list(data['upper_lip_color'])
    lower_lip_color = color_string_to_list(data['lower_lip_color'])

    colors = [hair_color, upper_lip_color, lower_lip_color]

    return colors


def get_source_from_request(request, allowed_extensions):
    data_key = 'source'

    if data_key not in request.files:
        flash('No file part')
        raise RuntimeError("No file was provided")

    source = request.files[data_key]

    if source.filename == '':
        flash('No selected file')
        raise RuntimeError("File was not selected")

    if not source or not is_allowed_file(source.filename, allowed_extensions):
        flash('Invalid file')
        raise RuntimeError("Invalid file")

    return source


def get_video_file_from_request(request, allowed_extensions):
    ensure_uploads_folder_exists()

    source = get_source_from_request(request, allowed_extensions)

    file_name = secure_filename(source.filename)
    full_file_path = os.path.join(get_uploads_folder_path(), file_name)
    source.save(full_file_path)

    return file_name


def get_image_from_request(request, allowed_extensions):
    source = get_source_from_request(request, allowed_extensions)

    np_arr = np.frombuffer(source.read(), np.uint8)
    img_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    return img_np, source.filename


