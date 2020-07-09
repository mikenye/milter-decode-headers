#!/usr/bin/env bash
# shellcheck shell=bash

docker build -t milter-decode-headers -f tests/Dockerfile .
