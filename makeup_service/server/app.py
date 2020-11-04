from flask import Flask
import os
import argparse
import makeup_service.server.views as views
from makeup_service.server.common import get_uploads_folder_path


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = get_uploads_folder_path()

app.add_url_rule('/', view_func=views.home, methods=['GET'])
app.add_url_rule('/image', view_func=views.process_image, methods=['GET', 'POST'])
app.add_url_rule('/video', view_func=views.process_video, methods=['GET', 'POST'])


def parse_args():
    parse = argparse.ArgumentParser()
    parse.add_argument('--host', default="0.0.0.0")
    parse.add_argument('--port', default=5000)

    return parse.parse_args()


if __name__ == '__main__':
    args = parse_args()

    host = args.host
    port = args.port

    app.run(host=host, port=port)
