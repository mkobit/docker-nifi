#!/usr/bin/env python3

import argparse
import logging
import string
import subprocess

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger('make_docker')

def template_properties(arg):
  props = arg.split(',')
  if not props:
    raise argparse.ArgumentTypeError('Template properties must be comma separated')
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

def write_template(template_file, substitions, destination_file):
  logger.info('Reading from template_file={}'.format(template_file.name))
  template = string.Template(template_file.read())
  logger.info('Substitutions for template={}'.format(substitions))
  content = template.substitute(substitions)
  logger.info('Writing to destination_file={}'.format(destination_file.name))
  destination_file.write(content)

def generate(args):
  logger.info('Beginning "generate" phase')
  with args.template_file as template_file, \
      args.destination_file as destination_file:
    write_template(template_file, args.template_substitutions, destination_file)
  logger.info('Ending "generate" phase')

def build(args):
  generate(args)
  logger.info('Beginning "build" phase')
  logger.info('Ending "build" phase')

def push(args):
  build(args)
  logger.info('Beginning "push" phase')
  logger.info('Ending "push" phase')

def add_generate_arguments(argument_group):
  argument_group.add_argument('--template-substitutions',
    type=template_properties,
    help='The template substitutions. Each substitution is a' \
    + ' key and value separated by an equal sign. Each' \
    + ' substitution is separated by a comma. For example, a' \
    + ' valid parameter would be "key1=value1,key2=value2"',
    required=True)
  argument_group.add_argument('-tmpl', '--template-file',
    type=argparse.FileType('r', encoding='UTF-8'),
    help='The template file', required=True)
  argument_group.add_argument('--destination-file', type=argparse.FileType('w',
    encoding='UTF-8'), help='Destination of rendered template file',
    required=True)

def add_build_arguments(argument_group):
  pass

def add_push_arguments(argument_group):
  pass

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Generate and build NiFi' \
    + 'docker image')
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

  # docker_args.add_argument('-r', '--repository', type=str, required=True,
  #   help='Repository to push results to')

  args = parser.parse_args()
  logger.setLevel(args.loggingLevel)
  logger.debug('Starting make_docker.py with args="{}"'.format(args))
  args.func(args)
