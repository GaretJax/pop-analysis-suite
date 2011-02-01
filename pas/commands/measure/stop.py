"""
``pas measure stop``
====================

**Usage:** ``pas jobmgr stop [-h] MEASURE_NAME``

positional arguments:
   .. cmdoption:: MEASURE_NAME

      The name of the measure to stop.

optional arguments:
  -h, --help   Show this help message and exit.

Stops all the measures on the different interfaces named ``MEASURE_NAME`` on all
hosts as defined by the ``interfaces`` and ``roles`` settings directives.

.. todo::
   Link to the settings reference.

The measures are stopped by sending the ``quit`` command to each named screen
session which matches the MEASURE_NAME and interface couple.
"""


from pas import commands
from pas import measure


# pylint: disable-msg=C0111
# Disable warning for the missing docstrings, there is not much to document
# here. For further information refer directly to the enclosed called function
# documentation.


def getparser(parser):
    parser.add_argument('name', metavar='MEASURE_NAME', help="The name of " \
                        "the measure to stop.")


@commands.select_case
def command(options):
    """
    Stops all the measures on the different interfaces named MEASURE_NAME on all
    hosts as defined by the interfaces and roles settings directives.
    """
    measure.stop(options.case[1])


