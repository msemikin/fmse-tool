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
from fmse_tool.cli.diagram_generator import generate_diagram
from docopt import docopt

from fmse_tool.cli.input_parser import parse_lts, parse_ctl_lts
from fmse_tool.AST.NotNode import NotNode
from fmse_tool.AST.TrueNode import TrueNode
from fmse_tool.AST.ExistsUntilNode import ExistsUntilNode
from fmse_tool.AST.ExistsGloballyNode import ExistsGloballyNode
from fmse_tool.AST.AtomicPropositionNode import AtomicPropositionNode


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
        light = parse_ctl_lts('./input/CTLLTS/light.txt')
        switch = parse_ctl_lts('./input/CTLLTS/switch.txt')
        composed = light.compose(switch)

        EF_lightOn = ExistsUntilNode(
            composed,
            TrueNode(),
            AtomicPropositionNode(composed, 'lightOn')
        )
        print('EF lightOn: ', EF_lightOn.evaluate(composed.get_states()))

        EG_Not_highBatteryUse = ExistsGloballyNode(
            composed,
            NotNode(
                composed,
                AtomicPropositionNode(composed, 'highBatteryUse')
            )
        )
        print('EG not highBatteryUse: ', EG_Not_highBatteryUse.evaluate(composed.get_states()))

        AG_EF_NOT_lightOn = NotNode(
            composed,
            ExistsUntilNode(
                composed,
                TrueNode(),
                NotNode(
                    composed,
                    ExistsUntilNode(
                        composed,
                        TrueNode(),
                        NotNode(
                            composed,
                            AtomicPropositionNode(
                                composed,
                                'lightOn'
                            )
                        )
                    )
                )
            )
        )
        print('AG EF not lightOn: ', AG_EF_NOT_lightOn.evaluate(composed.get_states()))

        AG_AF_highBatteryUse = NotNode(
            composed,
            ExistsUntilNode(
                composed,
                TrueNode(),
                NotNode(
                    composed,
                    ExistsGloballyNode(
                        composed,
                        NotNode(
                            composed,
                            AtomicPropositionNode(
                                composed,
                                'highBatteryUse'
                            )
                        )
                    )
                )
            )
        )
        print('AG AF highBatteryUse: ', AG_AF_highBatteryUse.evaluate(composed.get_states()))

        AG_highBatteryUse = NotNode(
            composed,
            ExistsUntilNode(
                composed,
                TrueNode(),
                NotNode(
                    composed,
                    AtomicPropositionNode(
                        composed,
                        'highBatteryUse'
                    )
                )
            )
        )
        print('AG highBatteryUse: ', AG_highBatteryUse.evaluate(composed.get_states()))






