"""
Executes the given test case on all client hosts.

If no test cases are provided and only one is available, it is executed; if
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
    commands.case_argument(parser)


@commands.select_case
def command(options):
    case.execute(options.case[1])