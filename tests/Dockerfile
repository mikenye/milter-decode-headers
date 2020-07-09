FROM mikenye/postfix

COPY decode-headers.py /decode-headers.py
COPY tests/test_milter_normal.expect /test_milter_normal.expect
COPY tests/run_tests.sh /run_tests.sh

ENV S6_CMD_WAIT_FOR_SERVICES=1

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
        && \
    pip3 install pymilter && \
    mkdir -p /output && \
    mkdir -p /etc/postfix/local_aliases && \
    echo "localdelivery /output/mail" > /etc/postfix/local_aliases/aliases && \
    echo "smtpd_milters = inet:127.0.0.1:8899" >> /etc/postfix/main.cf

CMD [ "/run_tests.sh" ]