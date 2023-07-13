#FROM python:3.10.0-alpine
#
#ENV PYTHONUNBUFFERED 1
#
#RUN apk add --update --no-cache postgresql-client python3-dev \
#  libffi-dev jpeg-dev freetype-dev libjpeg-turbo-dev libpng-dev \
#  curl libxml2-dev libxslt-dev libstdc++
#RUN apk add --update --no-cache --virtual .tmp-build-deps \
#  gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev \
#  g++
#
#RUN /usr/local/bin/python -m pip install --upgrade pip
#
#COPY ./requirements.txt /requirements.txt
#RUN pip install -r requirements.txt
#RUN apk del .tmp-build-deps
#
#WORKDIR /app
#COPY . /app
#
#RUN sed -i 's/\r$//g' /app/entrypoint.sh
#RUN chmod +x /app/entrypoint.sh
#
#ENTRYPOINT ["/app/entrypoint.sh"]

FROM python:3.11.0-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app
COPY . /app

RUN --mount=type=cache,id=custom-pip,target=/root/.cache/pip pip install -r /app/requirements.txt