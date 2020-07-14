FROM mikenye/postfix

COPY decode-headers.py /decode-headers.py
COPY requirements.txt /tmp/requirements.txt
COPY tests/test_milter_normal.expect /test_milter_normal.expect
COPY tests/test_milter_encoded.expect /test_milter_encoded.expect
COPY tests/run_tests.sh /run_tests.sh
COPY tests/milter_service_run /etc/services.d/decode-headers/run
COPY tests/milter_service_finish /etc/services.d/decode-headers/finish

ENV SYSLOG_PRIORITY=8

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
    pip3 install -r /tmp/requirements.txt && \
    mkdir -p /etc/postfix/local_aliases && \
    mkdir -p /output && \
    chmod a+w /output && \
    echo "localdelivery: /output/mail" > /etc/postfix/local_aliases/aliases && \
    useradd --system --no-create-home localdelivery

CMD [ "/run_tests.sh" ]
