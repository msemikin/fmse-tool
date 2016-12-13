"""LTS composer.

Usage:
  fmse_tool compose <file1> <file2>
  fmse_tool check
  fmse_tool (-h | --help)
  fmse_tool --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from docopt import docopt

from fmse_tool.cli.diagram_generator import generate_diagram, generate_extended_diagram
from fmse_tool.cli.input_parser import parse_lts, parse_ctl_lts_from_file
from fmse_tool.parsing import parser


def main():
    arguments = docopt(__doc__)

    if arguments['compose']:
        first_filename = arguments['<file1>']
        second_filename = arguments['<file2>']
        first_lts = parse_lts(first_filename)
        second_lts = parse_lts(second_filename)
        generate_diagram(first_lts, first_filename)
        generate_diagram(second_lts, second_filename)
        composed_lts = first_lts.compose(second_lts)
        generate_diagram(composed_lts, 'result')

    if arguments['check']:
        light = parse_ctl_lts_from_file('./input/CTLLTS/light.txt')
        switch = parse_ctl_lts_from_file('./input/CTLLTS/switch.txt')
        composed = light.compose(switch)
        generate_extended_diagram(composed, set(), 'result')

        tests = [
            "EF 'lightOn'",
            "EG !'highBatteryUse'",
            "AG EF !'lightOn'",
            "AG AF 'highBatteryUse'",
            "AG 'highBatteryUse'"
        ]

        for (i, test) in enumerate(tests):
            result = parser.parse(test).evaluate(composed, composed.get_states())
            generate_extended_diagram(composed, result, 'result' + str(i))
            print(test + ": " + str(result))






