"""
``pas run``
=================

**Usage:** ``pas run [-h]``

optional arguments:
  -h, --help  Show this help message and exit.

"""

import os

from pas import shell
from pas import commands
from pas.conf import settings


def getparser(parser):
    commands.case_argument(parser)
    parser.add_argument('targets', metavar='TARGET', nargs='*', help="The target to " \
                        "execute, defaults to 'run'.", default=[])


@commands.select_case
def command(options):
    """
    Exchanges the public keys between all VMs to allow direct ssh connections
    between them without user input.
    """
    local, _ = settings.PATHS['test-cases']

    shell.local("ENV_BASE='{2}' EXEC={0[1]} make -e -f {0[0]}/Makefile " \
                "{1}".format(options.case, " ".join(options.targets), settings.ENV_BASE))

