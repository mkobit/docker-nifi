#!/usr/bin/env bash

set -euo pipefail

if [ "${TRAVIS_PULL_REQUEST}" != "false" ]; then
  echo "Build Pull Request #${TRAVIS_PULL_REQUEST} => Branch [${TRAVIS_BRANCH}]"
  ./make_docker.py build \
    --template-file "${TEMPLATE_FILE}" \
    --template-substitutions "${TEMPLATE_VALUES}" \
    --destination-file "${DESTINATION}" \
    --repository "${DOCKER_REPOSITORY}" \
    --tags "${DOCKER_TAGS}"
elif [ "${TRAVIS_PULL_REQUEST}" == "false" -a "${TRAVIS_BRANCH}" == "master" ]; then
  echo "Build and Push Branch [${TRAVIS_BRANCH}] to Docker Hub with tags => [${DOCKER_TAGS}]"
  ./make_docker.py push \
    --template-file "${TEMPLATE_FILE}" \
    --template-substitutions "${TEMPLATE_VALUES}" \
    --destination-file "${DESTINATION}" \
    --repository "${DOCKER_REPOSITORY}" \
    --tags "${DOCKER_TAGS}" \
    --username "${DOCKER_USERNAME}" \
    --password "${DOCKER_PASSWORD}"
else
  echo "No action for [${TRAVIS_REPO_SLUG}]"
fi
