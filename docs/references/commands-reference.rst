.. _commands-reference:

Commands reference
==================

This section is dedicated to the description of the usage and the effects of
the different commands and subcommands bundled with the ``pas`` command line
tool.

.. todo::
   Double check all commands syntax and their effective inclusion in this
   document.

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

.. todo::
   Document the ``--settings`` option.

.. todo::
   Document the ``--verbose`` option.

.. todo::
   Document the ``--quiet`` option.

.. todo::
   Document the ``--host`` option and the ``HOST`` argument.

.. todo::
   Document the ``MEASURE_CASE`` argument.


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


Custom subcommands
------------------

The ``pas`` utility allows to define custom commands to extend the built-in set
of commands. The process of creating a new command and adding it to the ``pas``
utility is described in detail in the :ref:`command-subsystem` document.