.. _commands-reference:

Commands reference
==================

This section is dedicated to the description of the usage and the effects of
the different commands and subcommands bundled with the ``pas`` command line
tool.

The main ``pas`` command
------------------------

All operations involving the use of the ``pas`` command line utility require
the use of a subcommand, nonetheless some options common to all subcommands
can only be set directly on the main ``pas`` command.

The usage of the ``pas`` command (obtained running ``pas --help`` on the
command line) is the following::

   pas [-h] [--version] [-v] [-q] [--settings SETTINGS_MODULE]
         {authorize,execute,jobmgr,compile,init,measure,report} ...

subcommands:
   .. cmdoption:: authorize

      Exchanges the public keys between all VMs to allow direct ssh connections
      between them without user input.

   .. cmdoption:: compile

      Compiles the given test case on all hosts (by default) or on the hosts
      provided on the command line through the ``--host`` option.

   .. cmdoption:: execute

      Executes the given test case on all hosts having a role of ``client``
      (normally only one).

   .. cmdoption:: init

      Sets up a new measurement and analysis environment in the selected
      directory (or in the CWD if none is provided).

   .. cmdoption:: jobmgr

      Commands suite to remotely manage jobmgr instances.

   .. cmdoption:: measure

      Commands suite to execute measures and collect results.

   .. cmdoption:: report

      Commands suite process collected measure results.

optional arguments:
  -h, --help            Show this help message and exit.
  --version             Show program's version number and exit.
  -v, --verbose         Increments the verbosity (can be used multiple times).
  -q, --quiet           Decrements the verbosity (can be used multiple times).
  --settings SETTINGS_MODULE
                        The path to the settings module

The next two sections are dedicated to the description of some common arguments
and options and to the documentation of all built-in subcommands, respectively.

Common arguments and options
----------------------------

.. _settings options:

``--settings``
~~~~~~~~~~~~~~

The settings option lets you define the path to a directory containing the
``settings`` module (simply a ``settings.py`` file). This module is needed
by some commands to correctly identify a working environment.

It is possible to use this option when invoking a command from outside the
environment working directory.

It is also possible to set the path in the ``PAS_SETTINGS_MODULE`` shell
environment variable instead.

``--verbose`` and ``--quiet``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These flags increment and decrement the verbosity respectively and can be used
multiple times.

The short version ``-v`` and ``-q`` flags are also available.

``--host`` and ``[HOST]``
~~~~~~~~~~~~~~~~~~~~~~~~~

The host option or its argument alternative syntax are not a general ``pas``
argument but are used often enough by subcommands to being worth to be
documented here.

Many subcommands execute actions on remote machines. By default these actions
are carried out on a predefined list of hosts (normally all or all members of
a given role). Using this argument or the respective option variant, it is
possible to explicitly define one ore more hosts on which executed the command.

Both variants can be used multiple times to provide more than one host.

``MEASURE_CASE``
~~~~~~~~~~~~~~~~

A similar argument as made for the inclusion of the ``host`` argument or option
in this section can be made for the ``MEASURE_CASE`` argument too.

The ``MEASURE_CASE`` argument takes the name of a measure case from the cases
directory. In most cases the value is then coerced to a valid value using the
:func:`pas.commands.select_case` command decorator, which means that the value
can also be left out and the subcommand will prompt the user to select the 
desired value from a list of choices.


Built-in subcommands
--------------------

The following subcommands are already built-in and come bundled with all
``pas`` installations. In the next section is explained how it is possible to
add custom subcommands to an existing ``pas`` installation, on a global or
per-environment basis.

.. automodule:: pas.commands.init

.. automodule:: pas.commands.authorize

.. automodule:: pas.commands.compile

.. automodule:: pas.commands.execute

.. automodule:: pas.commands.jobmgr.start

.. automodule:: pas.commands.jobmgr.stop

.. automodule:: pas.commands.jobmgr.kill

.. automodule:: pas.commands.measure.start

.. automodule:: pas.commands.measure.stop

.. automodule:: pas.commands.measure.kill

.. automodule:: pas.commands.measure.collect

.. automodule:: pas.commands.report.toxml

.. automodule:: pas.commands.report.simplify

.. automodule:: pas.commands.report.decode

.. automodule:: pas.commands.report.report

.. automodule:: pas.commands.run


Custom subcommands
------------------

The ``pas`` utility allows to define custom commands to extend the built-in set
of commands. The process of creating a new command and adding it to the ``pas``
utility is described in detail in the :ref:`command-subsystem` document.