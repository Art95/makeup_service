from flask import request
from flask_socketio import send, emit
from makeup_service.server.request_processor import transform_video, transform_image, get_segmentation_for_image


def home():
    return "<h1>Makeup Service</h1><p>This site is a prototype API for makeup service application.</p>"


def process_image():
    if request.method == 'GET':
        return "<h1>Makeup Service</h1><p>This section is responsible for image processing.</p>"

    if request.method == 'POST':
        try:
            return transform_image(request)
        except RuntimeError as err:
            return str(err)


def process_video():
    if request.method == 'GET':
        return "<h1>Makeup Service</h1><p>This section is responsible for video processing.</p>"

    if request.method == 'POST':
        try:
            return transform_video(request)
        except RuntimeError as err:
            return str(err)


def send_segmentation(image):
    image_id = image['id']
    segmentation = get_segmentation_for_image(image)
    emit('segmentation', {'id': image_id, 'segmentation': segmentation})


def client_connect():
    print("Client connected")


def client_disconnect():
    print("Client disconnected")
