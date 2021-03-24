FROM python:3.9.2-alpine3.13

RUN apk add --no-cache \
        git \
        gcc \
        g++ \
        musl-dev \
    && pip3 install cve_bot==0.0.2 \
    && mkdir /cve_bot

COPY ./docker-entrypoint.sh /

ENTRYPOINT ["/docker-entrypoint.sh"]
