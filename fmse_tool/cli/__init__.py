"""LTS composer.

Usage:
  cli.py compose <file1> <file2>
  cli.py (-h | --help)
  cli.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from fmse_tool.cli.diagram_generator import generate_diagram
from docopt import docopt

from fmse_tool.cli.input_parser import parse_lts


def main():
    arguments = docopt(__doc__)

    print(arguments)
    first_filename = arguments['<file1>']
    second_filename = arguments['<file2>']
    first_lts = parse_lts(first_filename)
    second_lts = parse_lts(second_filename)
    generate_diagram(first_lts, first_filename)
    generate_diagram(second_lts, second_filename)
    composed_lts = first_lts.compose(second_lts)
    generate_diagram(composed_lts, 'result')

