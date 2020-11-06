from flask import Flask
import os
import argparse
from flask_socketio import SocketIO
import makeup_service.server.views as views

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.add_url_rule('/', view_func=views.home, methods=['GET'])
app.add_url_rule('/image', view_func=views.process_image, methods=['GET', 'POST'])
app.add_url_rule('/video', view_func=views.process_video, methods=['GET', 'POST'])

socketio = SocketIO(app)
socketio.on_event('connect', views.client_connect)
socketio.on_event('disconnect', views.client_disconnect)
socketio.on_event('image', views.send_segmentation, namespace='/stream')


def parse_args():
    parse = argparse.ArgumentParser()
    parse.add_argument('--host', default="127.0.0.1")
    parse.add_argument('--port', default=5000)
    parse.add_argument('--debug', default=True)

    return parse.parse_args()


if __name__ == '__main__':
    args = parse_args()

    host = args.host
    port = args.port
    debug = args.debug

    socketio.run(app, host=host, port=port, debug=debug)
