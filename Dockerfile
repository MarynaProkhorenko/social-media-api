FROM python:3.10-slim-buster
LABEL maintainer="maryna.prokhorenko11@gmail.com"

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /code


COPY requirements.txt /code/

RUN apt-get update && apt-get -y install libpq-dev gcc

Run pip install charset-normalizer
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /code/
