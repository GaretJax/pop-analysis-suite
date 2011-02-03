"""
``pas report report``
=====================

**Usage:** ``pas report report [-h] [MEASURE]``

positional arguments:
   .. cmdoption:: MEASURE

      The name of the collected measure for which to generate a report.

optional arguments:
  -h, --help   Show this help message and exit.

Generates an HTML report for the already collected, converted, simplified and
decoded measure named ``MEASURE``.

.. todo::
   Assemble all resources (not only one measure file) in the final report.
   Include things such as popc logs, different measures, highlighted source
   code,...
   
.. todo::
   Check syntax of all commands as they changed slightly

.. todo::
   Conditionally invoke tidy.
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
    Generates an HTML report for the already collected, converted, simplified
    and decoded measure named MEASURE.
    """
    measure.report(options.measure[1], options.case[0])

