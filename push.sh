#!/bin/bash
set -e

source .env

docker push elifesciences/metypeset:${IMAGE_TAG}
docker tag elifesciences/metypeset:${IMAGE_TAG} elifesciences/metypeset:latest
docker push elifesciences/metypeset:latest
