#!/usr/bin/env bash
# shellcheck shell=bash

echo "Waiting for postfix to become ready..."
sleep 10

/test_milter_normal.expect 127.0.0.1 25 test nobody@nowhere localdelivery@localdomain
sleep 10

ls -lah /output
cat /output/mail
sleep 10

echo "Finished"
exit 0
