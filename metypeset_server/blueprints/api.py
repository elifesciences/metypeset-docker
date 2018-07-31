import logging
import mimetypes

from flask import Blueprint, jsonify, request, Response, url_for
from werkzeug.exceptions import BadRequest

from metypeset_server.utils.mime_type_constants import MimeTypes

from ..metypeset.convert import convert_document, get_supported_mime_types


LOGGER = logging.getLogger(__name__)

DEFAULT_FILENAME = 'file'


def _get_filename_mimetype_and_content():
    data_type = None
    if not request.files:
        data_type = request.mimetype
        filename = request.args.get('filename')
        content = request.data
    elif 'file' not in request.files:
        raise BadRequest('missing file named "file", found: %s ' % request.files.keys())
    else:
        uploaded_file = request.files['file']
        data_type = uploaded_file.mimetype
        filename = uploaded_file.filename
        content = uploaded_file.read()
    if not content:
        raise BadRequest('no contents')

    if not filename:
        filename = '%s%s' % (DEFAULT_FILENAME, mimetypes.guess_extension(data_type) or '')
        LOGGER.debug('guessed filename %s for type %s', filename, data_type)
    elif data_type == 'application/octet-stream':
        data_type = mimetypes.guess_type(filename)[0]

    return filename, data_type, content


def create_api_blueprint(timeout=None):
    blueprint = Blueprint('api', __name__)

    supported_types = get_supported_mime_types()

    @blueprint.route("/convert", methods=['POST'])
    def _convert():
        filename, data_type, content = _get_filename_mimetype_and_content()

        if not filename:
            filename = '%s%s' % (DEFAULT_FILENAME, mimetypes.guess_extension(data_type) or '')
            LOGGER.debug('guessed filename %s for type %s', filename, data_type)
        elif data_type == 'application/octet-stream':
            data_type = mimetypes.guess_type(filename)[0]

        if data_type not in supported_types:
            error_message = 'unsupported type: %s (supported: %s)' % (
                data_type, ', '.join(sorted(supported_types))
            )
            LOGGER.info('%s (filename: %s)', error_message, filename)
            raise BadRequest(error_message)

        LOGGER.debug('processing file: %s (%d bytes, type "%s")', filename, len(content), data_type)
        conversion_result = convert_document(
            content=content,
            filename=filename,
            data_type=data_type,
            timeout=timeout
        )
        response_content = conversion_result['content']
        response_type = conversion_result['type']
        LOGGER.debug('response_content: %s (%s)', len(response_content), response_type)
        if response_type in {MimeTypes.TEI_XML, MimeTypes.JATS_XML}:
            response_type = 'text/xml'
        return Response(response_content, mimetype=response_type)

    @blueprint.route("/convert", methods=['GET'])
    def _convert_form():
        return '''
    <!doctype html>
    <title>Convert Document</title>
    <h1>Convert Document</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

    return blueprint
