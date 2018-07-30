import logging
import os
import subprocess
import sys
from tempfile import TemporaryDirectory
from pathlib import Path
from glob import glob

from ..utils.mime_type_constants import MimeTypes


LOGGER = logging.getLogger(__name__)


SUB_COMMAND_BY_MIME_TYPE_MAP = {
    MimeTypes.DOCX: 'docx',
    MimeTypes.DOC: 'doc',
    MimeTypes.DOTX: 'other',
    MimeTypes.RTF: 'other'
}


def get_supported_mime_types():
    return set(SUB_COMMAND_BY_MIME_TYPE_MAP.keys())


def get_metypeset_home():
    return os.environ.get('METYPESET_HOME')


def run_command(command, cwd=None, shell=False, timeout=None):
    try:
        LOGGER.info('command: %s (timeout=%s)', command, timeout)
        subprocess.run(
            command,
            stdout=sys.stdout,
            stderr=sys.stderr,
            cwd=cwd,
            shell=shell,
            check=True,
            timeout=timeout
        )
    except subprocess.CalledProcessError as e:
        LOGGER.error('command %s failed with %s, output=%s', command, e, e.output)
        raise e


def convert_document(filename, data_type, content, timeout=None):
    metypeset_home = get_metypeset_home()
    sub_command = SUB_COMMAND_BY_MIME_TYPE_MAP[data_type]
    with TemporaryDirectory(suffix='-metypeset') as path:
        p = Path(path)
        input_file = p.joinpath('file%s' % Path(filename).suffix)
        input_file.write_bytes(content)
        output_dir = p.joinpath('output')
        nlm_output_file = output_dir.joinpath('nlm/file.xml')
        command = [str(x) for x in [
            'python',
            Path(metypeset_home).joinpath('bin/meTypeset.py'),
            sub_command,
            input_file,
            output_dir
        ]]
        run_command(command, timeout=timeout)
        LOGGER.info('output files: %s', glob('%s/**/*' % output_dir, recursive=True))
        return {
            'type': MimeTypes.JATS_XML,
            'content': nlm_output_file.read_bytes()
        }
