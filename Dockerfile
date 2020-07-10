FROM debian:stable-slim

COPY decode-headers.py /decode-headers.py

ENV S6_BEHAVIOUR_IF_STAGE2_FAILS=2

RUN set -x && \
    apt-get update && \
    apt-get install --no-install-recommends -y \
        busybox-syslogd \
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
    # install s6 overlay
    curl -s https://raw.githubusercontent.com/mikenye/deploy-s6-overlay/master/deploy-s6-overlay.sh | sh && \
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

ENTRYPOINT [ "/init" ]

EXPOSE 8899/tcp
