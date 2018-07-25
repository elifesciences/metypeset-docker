#!/bin/bash

set -e

source .env

docker build -t elifesciences/metypeset -t elifesciences/metypeset:${IMAGE_TAG} \
  --build-arg METYPESET_TAG=${METYPESET_TAG} .
