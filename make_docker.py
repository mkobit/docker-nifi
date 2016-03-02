#!/usr/bin/env python3

import argparse
import logging
import string

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

def main(args):
  logger.debug('Starting make_docker.py with args="{}"'.format(args))
  with args.templateFile as templateFile:
    logger.info('Reading from templateFile={}'.format(templateFile.name))
    template = string.Template(templateFile.read())
  logger.info('Substitutions for template={}'.format(
              args.templateSubstitutions))
  content = template.substitute(args.templateSubstitutions)
  with args.destinationFile as destinationFile:
    logger.info('Writing to destinationFile={}'.format(destinationFile.name))
    destinationFile.write(content)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Generate and build NiFi' \
    + 'docker image')
  template_args = parser.add_argument_group('template arguments')
  template_args.add_argument('--templateSubstitutions',
                    type=template_properties,
                    help='The template substitutions. Each substitution is a' \
                    + ' key and value separated by an equal sign. Each' \
                    + ' substitution is separated by a comma. For example, a' \
                    + ' valid parameter would be "key1=value1,key2=value2"',
                    required=True)
  template_args.add_argument('-tpl', '--templateFile',
                    type=argparse.FileType('r', encoding='UTF-8'),
                    help='The template file', required=True)
  docker_args = parser.add_argument_group('Docker arguments')
  docker_args.add_argument('--destinationFile', type=argparse.FileType('w',
                    encoding='UTF-8'), help='Destination of templated' \
                    + ' dockerfile', required=True)
  docker_args.add_argument('--no-docker-build', action='store_true',
                    help='Do not build image')
  docker_args.add_argument('--no-docker-push', action='store_true',
                    help='Do not push Docker')
  docker_args.add_argument('-r', '--repository', type=str, required=True,
                    help='Repository to push results to')
  parser.add_argument('--loggingLevel', choices=['DEBUG', 'INFO',
                      'WARNING', 'ERROR', 'CRITICAL'], default='INFO',
                      help='Logging level to use')

  args = parser.parse_args()

  logger.setLevel(args.loggingLevel)
  main(args)
