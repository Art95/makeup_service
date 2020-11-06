import os
import io
import cv2
import pytest
import numpy as np
import tempfile

from makeup_service.server.app import app
from helpers.utils import get_test_files_folder_path


@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


def test_home(client):
    rv = client.get('/')
    assert b'<h1>Makeup Service</h1><p>This site is a prototype API for makeup service application.</p>' in rv.data


def test_image_home(client):
    rv = client.get('/image')
    assert b'<h1>Makeup Service</h1><p>This section is responsible for image processing.</p>' in rv.data


def test_video_home(client):
    rv = client.get('/video')
    assert b'<h1>Makeup Service</h1><p>This section is responsible for video processing.</p>' in rv.data


def test_process_image(client):
    test_image_path = os.path.join(get_test_files_folder_path(), 'test_image.jpg')

    with open(test_image_path, 'rb') as img:
        image_io = io.BytesIO(img.read())

    rv = client.post('/image', content_type='multipart/form-data',
                     data={
                         'hair_color': '255, 0, 0',
                         'upper_lip_color': '0, 255, 0',
                         'lower_lip_color': '0, 0, 255',
                         'source': (image_io, 'test_image.jpg')
                     },
                     follow_redirects=True)

    np_arr = np.frombuffer(rv.data, np.uint8)
    transformed_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    orig_image = cv2.imread(test_image_path)

    assert orig_image.shape == transformed_image.shape


def test_process_video(client):
    test_image_path = os.path.join(get_test_files_folder_path(), 'test_image.jpg')
    test_image = cv2.imread(test_image_path)
    frame_width = test_image.shape[1]
    frame_height = test_image.shape[0]
    frames_num = 5

    temp_video_source_file = tempfile.NamedTemporaryFile(suffix='.avi')

    out_video_stream = cv2.VideoWriter(temp_video_source_file.name, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10,
                                       (frame_width, frame_height))

    for i in range(frames_num):
        out_video_stream.write(test_image)

    out_video_stream.release()

    with open(temp_video_source_file.name, 'rb') as video:
        video_io = io.BytesIO(video.read())

    rv = client.post('/video', content_type='multipart/form-data',
                     data={
                         'hair_color': '255, 0, 0',
                         'upper_lip_color': '0, 255, 0',
                         'lower_lip_color': '0, 0, 255',
                         'source': (video_io, temp_video_source_file.name)
                     },
                     follow_redirects=True)

    temp_video_results_file = tempfile.NamedTemporaryFile(suffix='.avi')

    with open(temp_video_results_file.name, 'wb') as res_video_file:
        res_video_file.write(rv.data)

    cap = cv2.VideoCapture(temp_video_results_file.name)

    assert int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) == frames_num

    for i in range(frames_num):
        ret, image = cap.read()
        assert test_image.shape == image.shape

    cap.release()
