#!/bin/bash
set -e

docker run --rm elifesciences/metypeset /bin/bash -c \
  'pip install -r requirements.dev.txt && pytest'
