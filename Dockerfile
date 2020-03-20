FROM python:3.8-slim

WORKDIR /app

# Some application requirements require compiling
ADD requirements-compiled.txt /app/requirements-compiled.txt
RUN \
 apt-get update && \
 apt-get install -y --no-install-recommends build-essential libpq-dev libgdal-dev &&\
 # apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev g++ make && \
 pip install -r /app/requirements-compiled.txt --no-cache-dir && \
 apt-get autoremove -y build-essential && \
 rm -rf /var/lib/apt/lists/*
 # apk --purge del .build-deps

ADD requirements.txt /app/requirements.txt 
RUN pip install -r /app/requirements.txt
ADD requirements-dev.txt /app/requirements-dev.txt 
RUN pip install -r /app/requirements-dev.txt
ADD . /app
