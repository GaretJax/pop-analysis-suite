"""
``pas measure kill``
====================

**Usage:** ``pas measure kill [-h] [HOST [HOST ...]]``

positional arguments:
   .. cmdoption:: HOST

      Use this option to specify one or more hosts on which this command has to
      be run.

optional arguments:
  -h, --help   Show this help message and exit.

Kills all the running measures on the given host (or on all hosts if no host
is given) independently from the capturing interface or the name with which
they were started.
"""


from pas import commands
from pas import tshark
from pas import shell


# pylint: disable-msg=C0111
# Disable warning for the missing docstrings, there is not much to document
# here. For further information refer directly to the enclosed called function
# documentation.


def getparser(parser):
    commands.host_option(parser, argument=True)


def command(options):
    """
    Kills all the running measures on the given host (or on all hosts if no host
    is given) independently from the capturing interface or the name with which
    they were started.
    """
    with shell.workon(options.hosts):
        tshark.kill()

