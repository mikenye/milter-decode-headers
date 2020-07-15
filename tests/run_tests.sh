#!/usr/bin/env bash
# shellcheck shell=bash

LIGHTGREEN='\033[1;32m'
LIGHTRED='\033[1;31m'
LIGHTBLUE='\033[1;34m'
NOCOLOR='\033[0m'

EXITCODE=0

echo -e "${LIGHTBLUE}Waiting for postfix to become ready...${NOCOLOR}"
sleep 10

# Update postfix configuration
echo -e "${LIGHTBLUE}Updating postfix configuration for testing...${NOCOLOR}"
echo "smtpd_milters = inet:127.0.0.1:8899" >> /etc/postfix/main.cf && \
echo "mydestination = testserver" >> /etc/postfix/main.cf && \
postfix reload
sleep 5

# Send test email without subject encoding
echo -e "${LIGHTBLUE}Send test email without subject encoding...${NOCOLOR}"
/test_milter_normal.expect 127.0.0.1 25 test nobody@nowhere localdelivery@testserver > /dev/null 2>&1
sleep 10

alias CHECK_NOT_ENCODED="grep 'Subject: Test email normal' /output/mail > /dev/null 2>&1"
if CHECK_NOT_ENCODED; then
    echo -e "${LIGHTGREEN}PASSED normal email${NOCOLOR}"
else
    echo -e "${LIGHTRED}FAILED normal email${NOCOLOR}"
    EXITCODE=1
fi
rm /output/mail

# Send test email with subject encoding
echo -e "${LIGHTBLUE}Send test email with subject encoding...${NOCOLOR}"
/test_milter_encoded.expect 127.0.0.1 25 test nobody@nowhere localdelivery@testserver > /dev/null 2>&1
sleep 10

alias CHECK_ENCODED="grep -e 'X-Decoded-Subject: This is a utf-8 base64 encoded subject' -e 'X-Decoded-Subject-Encoding: utf-8' /output/mail > /dev/null 2>&1"
if CHECK_ENCODED; then
    echo -e "${LIGHTGREEN}PASSED encoded email${NOCOLOR}"
else
    echo -e "${LIGHTRED}FAILED encoded email${NOCOLOR}"
    EXITCODE=1
fi

sleep 10

echo -e "${LIGHTBLUE}Finished...${NOCOLOR}"
exit $EXITCODE
