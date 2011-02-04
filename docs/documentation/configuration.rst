.. _configuration:

Configuration
=============

The ``pas`` command line tool can be configured to customize its behavior to
better suit the user's needs. To achieve this, it reads configuration settings
from two distinct python modules:

 1. The first loaded module (which is always loaded) is the
    :mod:`pas.conf.basesettings` module; it contains all default settings as
    documented in the :ref:`settings reference`.
    
 2. Additionally, if a local settings module is found (either in the ``CWD`` or
    provided by the :ref:`--settings option <settings options>`), it is loaded
    too and overrides the values defined by the previous import.

Using this simple mechanism, it is possible to override the default settings
on a per-environment basis and to provide your own directives if needed by
any custom command.