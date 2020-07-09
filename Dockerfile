FROM debian:stable-slim

COPY decode-headers.py /decode-headers.py

RUN set -x && \
    apt-get update && \
    apt-get install --no-install-recommends -y \
        ca-certificates \
        curl \
        file \
        gcc \
        libmilter-dev \
        libmilter1.0.1 \
        libpython3.7-dev \
        python3 \
        python3-pip \
        python3-setuptools \
        python3-wheel \
        && \
    pip3 install pymilter && \
    # clean up
    apt-get remove -y \
        ca-certificates \
        curl \
        file \
        gcc \
        libmilter-dev \
        libpython3.7-dev \
        && \
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /src /tmp/* /var/lib/apt/lists/* && \
    find /var/log -type f -iname "*log" -exec truncate --size 0 {} \;    
