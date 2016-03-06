#!/usr/bin/env bash

set -e -x
LINT_ARGS="lint --no-interactive"
if [[ "$#" -gt 0 ]]; then
  LINT_ARGS="$@"
fi
docker run -it --rm -v $(pwd):/tmp/travis-workdir travis:nifi-docker-travis-cli ${LINT_ARGS}
