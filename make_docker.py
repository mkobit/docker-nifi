#!/usr/bin/env python3

import argparse
import logging
import string
import subprocess

logging.basicConfig(
  format='%(asctime)s - %(levelname)s - %(message)s',
  datefmt='%m/%d/%Y %I:%M:%S %p'
)
logger = logging.getLogger(__name__)

def template_properties(arg):
  props = arg.split(',')
  if not props:
    raise argparse.ArgumentTypeError('Template properties must be' \
      + ' comma separated')
  substitutions = dict()
  for prop in props:
    prop_split = prop.split('=')
    if len(prop_split) != 2:
      raise argparse.ArgumentTypeError('Format of each property should be' \
                            + ' "key=value". "{}" is not.'.format(prop))
    key, value = prop_split
    substitutions[key] = value
  if len(substitutions) != len(props):
    raise argparse.ArgumentTypeError('Unequal substitions for how many' \
                            + ' properties were specified. {}!={}'.format(
                            substitutions, props))
  return substitutions

def docker_tags(arg):
  tags = arg.split(',')
  if not tags:
    raise argparse.ArgumentTypeError('Must be at least 1 tag. Tags are' \
      + ' separated by commas')
  return tags

def write_template(template_file, substitions, destination_file):
  logger.info('Reading from template_file={}'.format(template_file.name))
  template = string.Template(template_file.read())
  logger.info('Template substitutions={}'.format(substitions))
  content = template.substitute(substitions)
  logger.info('Writing to destination_file={}'.format(destination_file.name))
  destination_file.write(content)

def generate_image_tags(repository, tags):
  for tag in tags:
    yield '{}:{}'.format(repository, tag)

def generate(args):
  logger.info('Beginning "generate" phase')
  substitutions = args.template_substitutions
  with args.template_file as template_file, \
      args.destination_file as destination_file:
    write_template(template_file, substitutions, destination_file)
  logger.info('Ending "generate" phase')

def build(args):
  generate(args)
  logger.info('Beginning "build" phase')
  filename = args.destination_file.name
  tags = args.tags
  repository = args.repository
  logger.info('Building dockerfile={} for repository={} with tags={}'.format(
    filename, repository, tags))
  for tag in generate_image_tags(repository, tags):
    args = ['docker', 'build', '--tag', tag, '--file', filename, '.']
    logger.info('Running subprocess with args={}'.format(args))
    # TODO: redirect subprocess output to logger
    subprocess.run(args, check=True)
  logger.info('Ending "build" phase')

def push(args):
  build(args)
  logger.info('Beginning "push" phase')
  username = args.username
  password = args.password
  tags = args.tags
  repository = args.repository
  dont_push = args.no_push

  if dont_push:
    logger.info('Skipping login. Not pushing built images.')
  else:
    login_args = ['docker', 'login', '--username', username,
      '--password', password]
    logger.info('Executing "docker login" with username={}'.format(username))
    completed_process = subprocess.run(login_args, check=False)
    if completed_process.returncode != 0:
      raise RuntimeError('Error running docker login. Return code={}'.format(
        completed_process.returncode))
  for tag in generate_image_tags(repository, tags):
    if dont_push:
      logger.info('Skipping push of docker image={}'.format(tag))
    else:
      logger.info('Pushing docker image={}'.format(tag))
      push_args = ['docker', 'push', tag]
      subprocess.run(push_args, check=True)
  logger.info('Ending "push" phase')

def add_generate_arguments(argument_group):
  argument_group.add_argument('--template-substitutions',
    type=template_properties,
    help='The template substitutions. Each substitution is a' \
    + ' key and value separated by an equal sign. Each' \
    + ' substitution is separated by a comma. For example, a' \
    + ' valid parameter would be "key1=value1,key2=value2"',
    metavar='KEY1=VALUE1,KEY2=VALUE2',
    required=True)
  argument_group.add_argument('--template-file',
    type=argparse.FileType('r', encoding='UTF-8'),
    help='The template file', required=True)
  argument_group.add_argument('--destination-file', type=argparse.FileType('w',
    encoding='UTF-8'), help='Destination of rendered template file',
    required=True)

def add_build_arguments(argument_group):
  argument_group.add_argument('--repository', type=str, required=True,
    help='Repository to push results to')
  argument_group.add_argument('--tags', type=docker_tags, required=True,
    help='Comma separated list of tags for the images')

def add_push_arguments(argument_group):
  argument_group.add_argument('--username', type=str, required=True,
    help='Docker Hub username')
  argument_group.add_argument('--password', type=str, required=True,
    help='Docker Hub password')
  argument_group.add_argument('--no-push', action='store_true',
    help='Does not push the built images to the remote')

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Publish NiFi docker images')
  parser.add_argument('--loggingLevel', choices=['DEBUG', 'INFO',
                      'WARNING', 'ERROR', 'CRITICAL'], default='INFO',
                      help='Logging level to use')
  subparsers = parser.add_subparsers(title='stages', description='Select a' \
    + ' stage from the lifecycle', help='Each stage is causes the previous' \
    + ' stages to be run as well')
  generate_parser = subparsers.add_parser('generate', help='Generate Dockerfile')
  generate_parser.set_defaults(func=generate)
  add_generate_arguments(
    generate_parser.add_argument_group('Template arguments'))

  build_parser = subparsers.add_parser('build', help='Generate and Build' \
    ' Docker Image')
  build_parser.set_defaults(func=build)
  add_generate_arguments(build_parser.add_argument_group('Template arguments'))
  add_build_arguments(build_parser.add_argument_group('Docker arguments'))

  push_parser = subparsers.add_parser('push', help='Generate, Build, and' \
    + ' Push Docker Image')
  push_parser.set_defaults(func=push)
  add_generate_arguments(push_parser.add_argument_group('Template arguments'))
  docker_arguments = push_parser.add_argument_group('Docker arguments')
  add_build_arguments(docker_arguments)
  add_push_arguments(docker_arguments)

  args = parser.parse_args()
  logger.setLevel(args.loggingLevel)
  logger.debug('Starting make_docker.py with args="{}"'.format(args))
  if 'func' in vars(args):
    args.func(args)
  else:
    parser.print_help()
