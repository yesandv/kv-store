FROM python:3.11

COPY . /app
WORKDIR /app

RUN apt-get update &&  \
    pip install --no-cache-dir --upgrade -r requirements.txt
