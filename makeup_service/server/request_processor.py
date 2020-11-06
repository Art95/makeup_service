import cv2
import io
import numpy as np
import tempfile
from flask import flash, send_file
from makeup_service.server.face_makeup_facade import FaceMakeupFacade

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

    video_file = get_video_file_from_request(request, allowed_extensions)
    transformed_temp_file = tempfile.NamedTemporaryFile(suffix=get_file_extension(video_file.name, True))

    face_makeup.apply_makeup_on_video(video_file.name, colors, save_to_file=True,
                                      out_file_path=transformed_temp_file.name)

    extension = get_file_extension(video_file.name)

    return send_file(transformed_temp_file.name, mimetype='video/' + extension)


def color_string_to_list(string):
    return list(map(int, string.split(',')))


def get_file_extension(file_name, with_dot=False):
    extension = file_name.split('.')[1]

    if with_dot:
        return '.' + extension
    else:
        return extension


def is_allowed_file(file_name, allowed_extensions):
    extension = get_file_extension(file_name)
    return extension in allowed_extensions


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
    source = get_source_from_request(request, allowed_extensions)

    source_video_temp_file = tempfile.NamedTemporaryFile(suffix=get_file_extension(source.filename, True))
    source.save(source_video_temp_file.name)

    return source_video_temp_file


def get_image_from_request(request, allowed_extensions):
    source = get_source_from_request(request, allowed_extensions)

    np_arr = np.frombuffer(source.read(), np.uint8)
    img_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    return img_np, source.filename

