# meTypeset Docker

A docker image for [meTypeset](https://github.com/MartinPaulEve/meTypeset).

## Pre-requistes

* [Docker](https://www.docker.com/)

## Build Container

```bash
docker-compose build
```

## Run Container

```bash
docker-compose up --build
```

```bash
docker run --rm -t -i -p 8074:8080 elifesciences/metypeset
```

## Server

```bash
curl -X POST --show-error --form \
  "file=@test.docx;filename=test.docx" \
  http://localhost:8074/api/convert
```

## CLI

```bash
docker run --rm -t -i -v"$(pwd):/data" elifesciences/metypeset \
  python bin/meTypeset.py docx /data/test.docx /data/output
```
