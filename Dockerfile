FROM python:3.6-stretch

ARG METYPESET_TAG=master
ENV METYPESET_HOME=/opt/meTypeset
ENV METYPESET_HOST=0.0.0.0
ENV METYPESET_PORT=8080

RUN apt-get update && \
  apt-get install -y unzip && \
  apt-get install -y default-jre

RUN wget \
  --output-document meTypeset.zip \
  https://github.com/MartinPaulEve/meTypeset/archive/${METYPESET_TAG}.zip && \
  unzip meTypeset.zip -d /tmp && \
  rm meTypeset.zip && \
  mv /tmp/meTypeset-${METYPESET_TAG} ${METYPESET_HOME}

WORKDIR ${METYPESET_HOME}

RUN pip install -r requirements.txt

COPY requirements.txt ./requirements.server.txt
RUN pip install -r requirements.server.txt

COPY metypeset_server/ ./metypeset_server
COPY healthcheck.sh requirements.dev.txt ./

CMD python -m metypeset_server.server

HEALTHCHECK --interval=10s --timeout=10s --retries=5 CMD ./healthcheck.sh
