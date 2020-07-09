#!/usr/bin/env sh
#shellcheck shell=sh

set -x

REPO=mikenye
IMAGE=milter-decode-headers
PLATFORMS="linux/386,linux/amd64,linux/arm/v7,linux/arm64"

docker context use x86_64
export DOCKER_CLI_EXPERIMENTAL="enabled"
docker buildx use homecluster

# Build latest
docker buildx build -t "${REPO}/${IMAGE}:latest" --compress --push --platform "${PLATFORMS}" .
