FROM mikenye/postfix

COPY decode-headers.py /decode-headers.py
COPY tests/test_milter_normal.expect /test_milter_normal.expect
COPY tests/run_tests.sh /run_tests.sh
COPY tests/milter_service_run /etc/services.d/decode-headers/run

RUN set -x && \
    apt-get update && \
    apt-get install --no-install-recommends -y \
        expect \
        gcc \
        libmilter-dev \
        libmilter1.0.1 \
        libpython3.7-dev \
        python3 \
        python3-pip \
        python3-setuptools \
        python3-wheel \
        telnet \
        && \
    pip3 install pymilter && \
    mkdir -p /etc/postfix/local_aliases && \
    mkdir -p /output && \
    chmod a+w /output && \
    echo "localdelivery: /output/mail" > /etc/postfix/local_aliases/aliases && \
    useradd --system --no-create-home localdelivery

# CMD [ "/run_tests.sh" ]
CMD [ "bash" ]