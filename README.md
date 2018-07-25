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
docker run -p 8074:8080 elifesciences/metypeset
```

## Server

```bash
curl -X POST --show-error --form \
  "file=@test.docx;filename=test.docx" \
  http://localhost:8074/api/convert
```

Note: the current image doesn't include `unoconv` and therefore only works with _docx_
(`application/vnd.openxmlformats-officedocument.wordprocessingml.document`).
