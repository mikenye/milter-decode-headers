#!/usr/bin/env bash
# shellcheck shell=bash

docker build -t milter-decode-headers -f tests/Dockerfile .

docker run \
    --rm \
    -d \
    -e POSTMASTER_EMAIL=postmaster@localdomain \
    -e POSTFIX_INET_PROTOCOLS=ipv4 \
    -e POSTFIX_MYDOMAIN=localdomain \
    -e POSTFIX_REJECT_INVALID_HELO_HOSTNAME=false \
    -e POSTFIX_REJECT_NON_FQDN_HELO_HOSTNAME=false \
    -e POSTFIX_REJECT_UNKNOWN_HELO_HOSTNAME=false \
    -e POSTFIX_SMTPUTF8_ENABLE=true \
    milter-decode-headers