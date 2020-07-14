#!/usr/bin/env bash
# shellcheck shell=bash

docker pull mikenye/postfix:development
docker build -t milter-decode-headers-test -f tests/Dockerfile .

docker run \
    --rm \
    --name milter-decode-headers \
    -it \
    -e POSTMASTER_EMAIL=postmaster@testserver \
    -e POSTFIX_INET_PROTOCOLS=ipv4 \
    -e POSTFIX_MYHOSTNAME=testserver \
    -e POSTFIX_REJECT_INVALID_HELO_HOSTNAME=false \
    -e POSTFIX_REJECT_NON_FQDN_HELO_HOSTNAME=false \
    -e POSTFIX_REJECT_UNKNOWN_HELO_HOSTNAME=false \
    -e POSTFIX_SMTPUTF8_ENABLE=true \
    milter-decode-headers-test
    