"""
Compiles the given test case on all hosts (by default) or on the hosts
provided on the command line through the --hosts option.

If no test cases are provided and only one is available, it is compiled; if
more are available, the user is presented with a list of available cases and
asked to make a choice.
"""


from pas import case
from pas import commands


# pylint: disable-msg=C0111
# Disable warning for the missing docstrings, there is not much to document
# here. For further information refer directly to the enclosed called function
# documentation.


def getparser(parser):
    commands.host_option(parser)
    commands.case_argument(parser)


@commands.select_case
def command(options):
    case.compile(options.case[1])

