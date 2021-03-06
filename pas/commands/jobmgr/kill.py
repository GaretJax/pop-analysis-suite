"""
``pas jobmgr kill``
====================

**Usage:** ``pas jobmgr kill [-h] [HOST [HOST ...]]``

positional arguments:
   .. cmdoption:: HOST

      Use this option to specify one or more hosts on which this command has to
      be run.

optional arguments:
  -h, --help   Show this help message and exit.

Kills the ``jobmgr`` on one or more hosts. If no hosts are provided, the
job managers are killed on all known hosts.
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
    Kills the jobmgr on one or more hosts.
    """
    if options.hosts:
        # Hosts manually defined, start them all without delays
        with shell.workon(options.hosts):
            jobmgr.kill()
    else:
        jobmgr.killall()

