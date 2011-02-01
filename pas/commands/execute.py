"""
``pas execute``
===============

**Usage:** ``pas execute [-h] [MEASURE_CASE]``

positional arguments:
   .. cmdoption:: MEASURE_CASE

      Measure case to execute on all client hosts.

optional arguments:
  -h, --help   Show this help message and exit.

Executes the given test case on all hosts having a role of ``client``
(normally only one).

If no measure case is provided and only one is available, it is compiled; if
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
    """
    Executes the given test case on all hosts having a role of client
    (normally only one).
    """
    case.execute(options.case[1])