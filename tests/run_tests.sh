#!/usr/bin/env bash
# shellcheck shell=bash

echo "Waiting for postfix to become ready..."
sleep 10

# Update postfix configuration
echo "smtpd_milters = inet:127.0.0.1:8899" >> /etc/postfix/main.cf && \
echo "mydestination = testserver" >> /etc/postfix/main.cf && \
postfix reload
sleep 5

# Send test email without subject encoding
/test_milter_normal.expect 127.0.0.1 25 test nobody@nowhere localdelivery@testserver
sleep 10

# Send test email with subject encoding
/test_milter_encoded.expect 127.0.0.1 25 test nobody@nowhere localdelivery@testserver
sleep 10

cat /output/mail
sleep 10

echo "Finished"
exit 0
