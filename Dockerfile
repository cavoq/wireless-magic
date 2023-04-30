FROM python:latest

RUN apt-get update

COPY . /twiner

WORKDIR /twiner

RUN make run