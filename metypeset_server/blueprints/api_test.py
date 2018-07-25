from __future__ import absolute_import

from contextlib import contextmanager
import logging
import json
from io import BytesIO
from unittest.mock import patch, MagicMock

from flask import Flask
from werkzeug.exceptions import BadRequest

import pytest

from ..utils.mime_type_constants import MimeTypes

from . import api as api_module
from .api import (
    create_api_blueprint,
    DEFAULT_FILENAME
)


LOGGER = logging.getLogger(__name__)

DEFAULT_CONFIG = {}

PDF_FILENAME = 'test.pdf'
PDF_CONTENT = b'eat pdf for breakfast'
XML_CONTENT = b'<article></article>'

DOCX_FILENAME = 'test.docx'
DOCUMENT_CONTENT = b'dummy content'


@pytest.fixture(name='test_client')
def _api_test_client():
    blueprint = create_api_blueprint()
    app = Flask(__name__)
    app.register_blueprint(blueprint)
    yield app.test_client()


@pytest.fixture(name='convert_document_mock', autouse=True)
def _convert_document():
    with patch.object(api_module, 'convert_document') as convert_document_mock:
        yield convert_document_mock


@pytest.fixture(name='pipeline_runner')
def _pipeline_runner(create_simple_pipeline_runner_from_config):
    return create_simple_pipeline_runner_from_config.return_value


def _get_json(response):
    return json.loads(response.data.decode('utf-8'))


def _get_ok_json(response):
    assert response.status_code == 200
    return _get_json(response)


class TestApiBlueprint(object):
    class TestConvert(object):
        def test_should_show_form_on_get(self, test_client):
            response = test_client.get('/convert')
            assert response.status_code == 200
            assert b'html' in response.data

        def test_should_reject_post_without_data(self, test_client):
            response = test_client.post('/convert')
            assert response.status_code == BadRequest.code

        def test_should_reject_post_with_empty_document(self, test_client):
            response = test_client.post('/convert', content_type=MimeTypes.DOCX)
            assert response.status_code == BadRequest.code

        def test_should_reject_post_with_wong_type(self, test_client):
            response = test_client.post('/convert', data=DOCUMENT_CONTENT, content_type='other')
            assert response.status_code == BadRequest.code

        def test_should_reject_file_with_wrong_name(self, test_client):
            response = test_client.post(
                '/convert', data=dict(
                    otherfile=(BytesIO(DOCUMENT_CONTENT), DOCX_FILENAME)
                )
            )
            assert response.status_code == BadRequest.code

        def test_should_accept_file_and_pass_to_convert_method(
            self, test_client, convert_document_mock):

            convert_document_mock.return_value = {
                'content': XML_CONTENT,
                'type': MimeTypes.JATS_XML
            }
            response = test_client.post('/convert', data=dict(
                file=(BytesIO(DOCUMENT_CONTENT), DOCX_FILENAME),
            ))
            convert_document_mock.assert_called_with(
                content=DOCUMENT_CONTENT,
                filename=DOCX_FILENAME,
                data_type=MimeTypes.DOCX
            )
            assert response.status_code == 200
            assert response.data == XML_CONTENT

        def test_should_accept_post_data_and_pass_to_convert_method(
            self, test_client, convert_document_mock):

            convert_document_mock.return_value = {
                'content': XML_CONTENT,
                'type': MimeTypes.JATS_XML
            }
            response = test_client.post(
                '/convert?filename=%s' % DOCX_FILENAME,
                data=DOCUMENT_CONTENT,
                content_type=MimeTypes.DOCX
            )
            convert_document_mock.assert_called_with(
                content=DOCUMENT_CONTENT,
                filename=DOCX_FILENAME,
                data_type=MimeTypes.DOCX
            )
            assert response.status_code == 200
            assert response.data == XML_CONTENT

        def test_should_accept_post_data_without_filename(
            self, test_client, convert_document_mock):

            convert_document_mock.return_value = {
                'content': XML_CONTENT,
                'type': MimeTypes.JATS_XML
            }
            response = test_client.post(
                '/convert',
                data=DOCUMENT_CONTENT,
                content_type=MimeTypes.DOCX
            )
            convert_document_mock.assert_called_with(
                content=DOCUMENT_CONTENT,
                filename='%s.docx' % DEFAULT_FILENAME,
                data_type=MimeTypes.DOCX
            )
            assert response.status_code == 200
            assert response.data == XML_CONTENT
