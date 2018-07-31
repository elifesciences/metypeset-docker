import argparse
import logging
import os

from flask import Flask
from flask_cors import CORS

from .blueprints.api import (
    create_api_blueprint
)


LOGGER = logging.getLogger(__name__)


DEFAULT_TIMEOUT = 60


class EnvVarNames:
    HOST = 'METYPESET_HOST'
    PORT = 'METYPESET_PORT'
    TIMEOUT = 'METYPESET_TIMEOUT'


def create_app(timeout):
    app = Flask(__name__)
    CORS(app)

    api = create_api_blueprint(timeout=timeout)
    app.register_blueprint(api, url_prefix='/api')

    return app


def initialize_logging():
    logging.basicConfig(level='DEBUG')
    logging.getLogger('summa.preprocessing.cleaner').setLevel(logging.WARNING)


def main(argv=None):
    host = os.environ.get(EnvVarNames.HOST, '0.0.0.0')
    port = int(os.environ.get(EnvVarNames.PORT, '8080'))
    timeout = int(os.environ.get(EnvVarNames.TIMEOUT, DEFAULT_TIMEOUT))
    app = create_app(timeout=timeout)
    app.run(port=port, host=host, threaded=True)


if __name__ == "__main__":
    initialize_logging()

    main()
