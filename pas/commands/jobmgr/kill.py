from pas import commands
from pas import jobmgr
from pas import shell


# pylint: disable-msg=C0111
# Disable warning for the missing docstrings, there is not much to document
# here. For further information refer directly to the enclosed called function
# documentation.


def getparser(parser):
    commands.host_option(parser)


def command(options):
    if options.hosts:
        # Hosts manually defined, start them all without delays
        with shell.workon(options.hosts):
            jobmgr.kill()
    else:
        jobmgr.killall()

