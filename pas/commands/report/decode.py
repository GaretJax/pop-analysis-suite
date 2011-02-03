"""
.. _pas-report-decode:

``pas report decode``
=====================

**Usage:** ``pas report decode [-h] [MEASURE] [MEASURE_CASE]``

positional arguments:
   .. cmdoption:: MEASURE

      The name of the collected measure to decode.

   .. cmdoption:: MEASURE_CASE

      The name of the measure case from which this measure was run. This is
      needed to be able to use the additionally defined types for the measured
      binary.

optional arguments:
  -h, --help   Show this help message and exit.

Decodes the results of an already collected and simplified measure by
annotating the XML structure with the needed POP metadata, as extracted from
the TCP payload.

The decoding additional custom types can be defined on a per-environment basis.

.. todo::
   Document and link to the custom types + settings directive parser extension 
   model.

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
    commands.case_argument(parser)


@commands.select_measure
@commands.select_case
def command(options):
    """
    Decodes the results of an already collected and simplified measure by
    annotating the XML structure with the needed POP metadata, as extracted from
    the TCP payload.
    """
    measure.decode(options.measure[1], options.case[0])

