#!/usr/bin/env bash

set -e -x
docker build -f Dockerfile-travis-lint -t travis:lint .
