FROM python:3.9.2-alpine3.13

RUN apk add --no-cache git \
    && pip3 install cve_bot==0.0.1

ENTRYPOINT ["dikort"]
