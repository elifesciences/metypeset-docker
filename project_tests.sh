#!/bin/bash
set -e

docker run --rm elifesciences/metypeset:${IMAGE_TAG} /bin/bash -c \
  'pip install -r requirements.dev.txt && pytest'
