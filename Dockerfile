FROM python:3.9.2-alpine3.13

RUN apk add --no-cache \
        git \
        gcc \
        g++ \
        musl-dev \
    && pip3 install cve-bot==0.0.5 \
    && mkdir /cve_bot

COPY ./docker-entrypoint.sh /
WORKDIR /cve_bot

ENV CVE_BOT_DB_PATH=/cve_bot/main.db

ENTRYPOINT ["/docker-entrypoint.sh"]
