"""
``pas measure collect``
=======================

**Usage:** ``pas measure collect [-h] MEASURE_NAME``

positional arguments:
   .. cmdoption:: MEASURE_NAME

      The name to give to the collected measure.

optional arguments:
  -h, --help   Show this help message and exit.

Collects the results of a measure by copying the remote files resulting from
the last run measure to the local measures folder and by organizing them by
host ip address.

This process does not alter the remote files, it is thus possible to repeat a 
``collect`` command different times until a new measure is not started.
"""


from pas import measure


# pylint: disable-msg=C0111
# Disable warning for the missing docstrings, there is not much to document
# here. For further information refer directly to the enclosed called function
# documentation.


def getparser(parser):
    parser.add_argument('name', metavar='MEASURE_NAME', help="The name to " \
                        "give to the collected measure.")


def command(options):
    measure.collect(options.name)


