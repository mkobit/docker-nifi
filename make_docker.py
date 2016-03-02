#!/usr/bin/env python3

import argparse

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Generate and build NiFi' \
    + 'docker image')
  # template file
  parser.add_argument("--no-docker-build", action="store_true",
                    help="Do not build image")
  parser.add_argument("--no-docker-push", action="store_true",
                    help="Do not push Docker")
  parser.add_argument("-r", "--repository", type=str, required=True,
                    help="Repository name")
  args = parser.parse_args()
  print(args)
