#!/usr/bin/env bash
# shellcheck shell=bash

LIGHTGREEN='\033[1;32m'
LIGHTRED='\033[1;31m'
NOCOLOR='\033[0m'

echo "Waiting for postfix to become ready..."
sleep 10

# Update postfix configuration
echo "smtpd_milters = inet:127.0.0.1:8899" >> /etc/postfix/main.cf && \
echo "mydestination = testserver" >> /etc/postfix/main.cf && \
postfix reload
sleep 5

# Send test email without subject encoding
/test_milter_normal.expect 127.0.0.1 25 test nobody@nowhere localdelivery@testserver > /dev/null 2>&1
sleep 10

cat /output/mail | grep 'Subject: Test email normal' > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
    echo -e "${LIGHTGREEN}PASSED normal email${NOCOLOR}"
else
    echo -e "${LIGHTRED}FAILED normal email${NOCOLOR}"
fi
rm /output/mail

# Send test email with subject encoding
/test_milter_encoded.expect 127.0.0.1 25 test nobody@nowhere localdelivery@testserver > /dev/null 2>&1
sleep 10

cat /output/mail | grep -e 'X-Decoded-Subject: This is a utf-8 base64 encoded subject' -e 'X-Decoded-Subject-Encoding: utf-8'  > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
    echo -e "${LIGHTGREEN}PASSED encoded email${NOCOLOR}"
else
    echo -e "${LIGHTRED}FAILED encoded email${NOCOLOR}"
fi

cat /output/mail 
sleep 10

echo "Finished"
exit 0
