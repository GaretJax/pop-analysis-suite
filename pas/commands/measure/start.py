"""
``pas measure start``
=====================

**Usage:** ``pas jobmgr start [-h] MEASURE_NAME``

positional arguments:
   .. cmdoption:: MEASURE_NAME

      The name to give to the newly started measure.

optional arguments:
  -h, --help   Show this help message and exit.

Starts a new measure on all hosts and for each interface as defined in the
settings ``interfaces`` and ``roles`` directives.

.. todo::
   Link to the settings reference.

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


def getparser(parser):
    parser.add_argument('name', metavar='MEASURE_NAME', help="The name to " \
                        "give to the newly started measure.")


def command(options):
    """
    Starts a new measure on all hosts as defined in the settings interfaces and
    roles directives.
    """
    measure.start(options.name)


