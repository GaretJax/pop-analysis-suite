"""
``pas measure start``
=====================

**Usage:** ``pas jobmgr start [-h]``

optional arguments:
  -h, --help   Show this help message and exit.

Starts a new measure on all hosts and for each interface as defined in the
:data:`INTERFACES <pas.conf.basesettings.INTERFACES>` and :data:`ROLES
<pas.conf.basesettings.ROLES>` settings directives.

The measure is started in a detached named screen session to be able to
disconnect from the remote host while letting the measure run. The same name
can then also be used to cleanly stop or to kill the measure.

All existing measure files in the remote measure desintation directory will be
erased without asking for confirmations! Make sure to have collected all
previously run measures you don't want to lose.

Note that it is not possible to run parallel measures (and it doesn't make much
sens, as both tshark process will capture all the traffic).
"""


from pas import measure


# pylint: disable-msg=C0111
# Disable warning for the missing docstrings, there is not much to document
# here. For further information refer directly to the enclosed called function
# documentation.


def command(options):
    """
    Starts a new measure on all hosts as defined in the settings INTERFACES and
    ROLES directives.
    """
    measure.start('pas')


