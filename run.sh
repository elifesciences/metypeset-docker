#!/bin/bash

set -e

source .env

docker run \
    --rm \
    --name metypeset \
    -p 8074:${METYPESET_PORT} \
    elifesciences/metypeset:${IMAGE_TAG} \
    $@
