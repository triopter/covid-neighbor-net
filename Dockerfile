FROM python:3.8-alpine

WORKDIR /app

# Some application requirements require compiling
ADD requirements-compiled.txt /app/requirements-compiled.txt
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev g++ make gdal-dev && \
 pip install -r /app/requirements-compiled.txt --no-cache-dir && \
 apk --purge del .build-deps

ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
ADD . /app
