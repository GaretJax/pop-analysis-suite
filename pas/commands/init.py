"""
Sets up a new measurement and analysis environment in the selected directory
(the CWD if none is provided).

The directory has not to exist or to exsist and be empty for the command to
succeed.

The environment is set up mostly by recursively copying all the files inside
pas.conf.suite_template to the newly created directory.
"""


import os
import logging

from pas import env
from pas import commands


# pylint: disable-msg=C0111
# Disable warning for the missing docstrings, there is not much to document
# here. For further information refer directly to the enclosed called function
# documentation.


def getparser(parser):
    parser.add_argument('dir', nargs='?', default='.', type=str,
                        help='the directory inside which create the suite')

@commands.nosettings
def command(options):
    log = logging.getLogger('CommandLogger')
    dest = os.path.realpath(options.dir)
    
    log.info("Attempting to create a new environment in '%s'...", dest)

    if os.path.exists(dest):
        # If the path already exists, make sure it is a directory and it is
        # empty.
        if not os.path.isdir(dest):
            log.critical("The selected path is not a directory.")
            return 1

        if os.listdir(dest):
            log.critical("The selected directory is not empty.")
            return 1
    else:
        # Create the directory
        try:
            os.mkdir(dest)
        except OSError as e:
            log.critical("An error occurred while creating the directory to" \
                         " host the environment (%s: %s).", e.errno, e.strerror)
            return 1
    
    env.setup(dest)

    log.info("Done.")

