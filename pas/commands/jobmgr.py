"""
Various job manager management commands. The available commands (start, stop,
restart and kill) are directly mapped to the pas.jobmgr.* functions.

If no hosts are provided, "all" is appended to the given commands to execute
them in the right order with the necessary delays. Refer to the
pas.jobmgr.*all functions to obtain further details.

When one or more hosts are provided using the --hosts option, then the
commands will be executed directly on all hosts, in the order given on the
command line and without any delays.
"""


from pas import commands
from pas import jobmgr
from pas import shell


# pylint: disable-msg=C0111
# Disable warning for the missing docstrings, there is not much to document
# here. For further information refer directly to the enclosed called function
# documentation.


def getparser(parser):
    commands.host_option(parser)
    parser.add_argument('actions', metavar='command', nargs='+',
                        choices=['start', 'stop', 'restart', 'kill'])


def command(options):
    if options.hosts:
        # Hosts manually defined, start them all without delays
        with shell.workon(options.hosts):
            for action in options.actions:
                getattr(jobmgr, action)()
    else:
        for action in options.actions:
            getattr(jobmgr, action + "all")()

