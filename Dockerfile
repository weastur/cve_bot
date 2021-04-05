FROM python:3.9.3-alpine3.13

ARG VERSION

RUN apk add --no-cache \
        git \
        gcc \
        g++ \
        musl-dev \
    && pip3 install cve-bot==${VERSION} \
    && mkdir /cve_bot

COPY ./docker-entrypoint.sh /
WORKDIR /cve_bot

ENV CVE_BOT_DB_PATH=/cve_bot/main.db

ENTRYPOINT ["/docker-entrypoint.sh"]
