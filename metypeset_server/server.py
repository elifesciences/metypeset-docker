import argparse
import logging
import os

from flask import Flask
from flask_cors import CORS

from .blueprints.api import (
    create_api_blueprint
)


LOGGER = logging.getLogger(__name__)

class EnvVarNames:
    HOST = 'METYPESET_HOST'
    PORT = 'METYPESET_PORT'


def create_app():
    app = Flask(__name__)
    CORS(app)

    api = create_api_blueprint()
    app.register_blueprint(api, url_prefix='/api')

    return app


def initialize_logging():
    logging.basicConfig(level='DEBUG')
    logging.getLogger('summa.preprocessing.cleaner').setLevel(logging.WARNING)


def main(argv=None):
    app = create_app()
    host = os.environ.get(EnvVarNames.HOST, '0.0.0.0')
    port = int(os.environ.get(EnvVarNames.PORT, '8080'))
    app.run(port=port, host=host, threaded=True)


if __name__ == "__main__":
    initialize_logging()

    main()
