from flask import Flask
import os
import argparse
import makeup_service.server.views as views

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.add_url_rule('/', view_func=views.home, methods=['GET'])
app.add_url_rule('/image', view_func=views.process_image, methods=['GET', 'POST'])
app.add_url_rule('/video', view_func=views.process_video, methods=['GET', 'POST'])


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

    app.run(host=host, port=port, debug=debug)
