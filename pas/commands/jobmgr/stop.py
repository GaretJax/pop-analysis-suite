"""
``pas jobmgr stop``
====================

**Usage:** ``pas jobmgr stop [-h] [HOST [HOST ...]]``

positional arguments:
   .. cmdoption:: HOST

      Use this option to specify one or more hosts on which this command has to
      be run.

optional arguments:
  -h, --help   Show this help message and exit.

Stops the ``jobmgr`` on one or more hosts.

If no hosts are provided, then the command first stops the ``child`` hosts
and then, after accounting for a shutdown delay, the ``master`` hosts.

If one or more hosts are provided, the ``stop`` command is sent to all hosts at
the same time.
"""

from pas import commands
from pas import jobmgr
from pas import shell


# pylint: disable-msg=C0111
# Disable warning for the missing docstrings, there is not much to document
# here. For further information refer directly to the enclosed called function
# documentation.


def getparser(parser):
    commands.host_option(parser, argument=True)


def command(options):
    """
    Stops the jobmgr on the provided hosts. If no hosts are provided, stops
    the jobmgr on all master and client hosts by accounting for a shutdown
    delay.
    """
    if options.hosts:
        # Hosts manually defined, start them all without delays
        with shell.workon(options.hosts):
            jobmgr.stop()
    else:
        jobmgr.stopall()

