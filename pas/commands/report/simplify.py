"""
``pas report simplify``
=======================

**Usage:** ``pas report simplify [-h] [MEASURE]``

positional arguments:
   .. cmdoption:: MEASURE

      The name of the collected measure to simplify.

optional arguments:
  -h, --help   Show this help message and exit.

Converts the results of an already collected and converted measure from the 
wireshark XML format to a simplified POP oriented XML format.

If ``MEASURE`` is not provided, the user is presented with a list of already
collected measures and asked to make a choice.
"""


from pas import commands
from pas import measure


# pylint: disable-msg=C0111
# Disable warning for the missing docstrings, there is not much to document
# here. For further information refer directly to the enclosed called function
# documentation.


def getparser(parser):
    commands.measure_argument(parser)


@commands.select_measure
def command(options):
    """
    Converts the results of an already collected and converted measure from the 
    wireshark XML format to a simplified POP oriented XML format.
    """
    measure.simplify(options.measure[1])

