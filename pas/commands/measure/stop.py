"""
``pas measure stop``
====================

**Usage:** ``pas jobmgr stop [-h]``

optional arguments:
  -h, --help   Show this help message and exit.

Stops the measures running on all hosts and for each interface as defined in
the :data:`INTERFACES <pas.conf.basesettings.INTERFACES>` and :data:`ROLES
<pas.conf.basesettings.ROLES>` settings directives.

The measures are stopped by sending the ``quit`` command to each named screen
session which matches the MEASURE_NAME and interface couple.
"""


from pas import commands
from pas import measure


# pylint: disable-msg=C0111
# Disable warning for the missing docstrings, there is not much to document
# here. For further information refer directly to the enclosed called function
# documentation.


def command(options):
    """
    Stops the measures running on all hosts and for each interface as defined in
    the INTERFACES and ROLES settings directives.
    """
    measure.stop('pas')


