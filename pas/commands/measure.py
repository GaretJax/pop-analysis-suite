"""
Measure management commands. Commands are provided to start, stop or kill a
measure process.

The start and stop commands automatically operate on the hosts as specified
in the roles settings directive, while (by default) the kill command kills all
measures on all hosts.

The --host option is only taken into account when calling the kill command
and allows to specify a comma separated lists of hosts on which the measures
have to be killed.
"""


from pas import case
from pas import commands
from pas import measure
from pas import shell
from pas import tshark


# pylint: disable-msg=C0111
# Disable warning for the missing docstrings, there is not much to document
# here. For further information refer directly to the enclosed called function
# documentation.


def getparser(parser):
    parser.add_argument('action', metavar='command', choices=['start', 'stop',
                        'kill', 'collect', 'toxml', 'simplify', 'decode',
                        'report'])
    commands.case_or_measure_argument(parser)
    commands.host_option(parser)


def command(options):
    if options.action == 'kill':
        with shell.workon(options.hosts):
            tshark.kill()
        return
    elif options.action in ('start', 'stop', 'collect'):
        _, name = case.select(options.case_or_measure)
    else:
        _, name = measure.select(options.case_or_measure)
    
    getattr(measure, options.action)(name)


