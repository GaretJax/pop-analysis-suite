"""
.. _pas-compile:

``pas compile``
===============

**Usage:** ``pas compile [-h] [--host HOST] [MEASURE_CASE]``

positional arguments:
   .. cmdoption:: MEASURE_CASE

      Measure case to compile on the different hosts.

optional arguments:
  -h, --help   Show this help message and exit.
  --host HOST  Use this option to specify one or more hosts on which this
               command has to be run. The --host option can be specifed
               multiple times to define multiple hosts.

Compiles the given test case on all hosts (by default) or on the hosts
provided on the command line through the ``--host`` option.

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
    commands.host_option(parser)
    commands.case_argument(parser)


@commands.select_case
def command(options):
    """
    Compiles the given test case on all hosts (by default) or on the hosts
    provided on the command line through the --host option.
    """
    case.compile(options.case[1])

