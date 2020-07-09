FROM debian:stable-slim

COPY decode-headers.py /decode-headers.py

RUN set -x && \
    apt-get update && \
    apt-get install --no-install-recommends -y \
        gcc \
        libmilter-dev \
        libmilter1.0.1 \
        libpython3.7-dev \
        python3 \
        python3-pip \
        python3-setuptools \
        python3-wheel \
        && \
    pip3 install pymilter
