#!/usr/bin/env bash

set -euo pipefail

readonly travis_image_name='travis:nifi-docker-travis-cli'

readonly script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [[ "$(docker images -q ${travis_image_name} 2> /dev/null)" == "" ]]; then
  echo "Image ${travis_image_name} does not exist locally yet, building first."
  docker build -f ${script_dir}/Dockerfile-travis -t travis:nifi-docker-travis-cli ${script_dir}
fi

LINT_ARGS="lint --no-interactive"
if [[ "$#" -gt 0 ]]; then
  LINT_ARGS="$@"
fi
docker run -it --rm -v ${script_dir}:/tmp/travis-workdir travis:nifi-docker-travis-cli ${LINT_ARGS}
