FROM ubuntu:latest

RUN apt-get update && \
    apt-get -y install build-essential cmake

COPY . /evil-twin

WORKDIR /evil-twin

RUN make build

CMD ["./evil-twin"]