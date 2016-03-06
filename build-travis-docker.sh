#!/usr/bin/env bash

set -e -x
docker build -f Dockerfile-travis -t travis:nifi-docker-travis-cli .
