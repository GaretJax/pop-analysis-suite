.. _command-subsystem:

The command subsystem
=====================

The ``pas`` commands can be grouped into 4 areas of interest:

Meta management
   Allows to execute all actions to setup and manage a testing environment and
   its configuration.
 
Jobmgr management
   Provides a simple interface to manage remote ``jobmgr`` processes (start,
   stop, kill,...).
 
Measuring
   Collection of commands to manage the measuring process, such as starting or
   stopping a measure.
 
Processing
   Different tools to act upon al already acquired measure, to transform,
   simplify, filter, etc. the different assets resulting from a measuring
   process.

A fifth group, the **derived commands** group can also be added and contains
all custom defined workflows resulting from the chaining of different
"primitive" commands.

.. todo::
   Make sure this is actually possible, the current implementation does not
   provide hooks or facilities to work on composite commands.


.. _architecture:

Architecture
------------

The various available commands are gathered at runtime by the ``pas`` binary
(oh, well… actually it is a python script) when executed. The entry point
recursively scans the ``pas.commands`` package to retrieve the various commands.

This mechanism allows for great flexibility in the definition of parsers for 
single commands and makes the addition of a new command relatively easy.

The next chapter will show you how to create a new command by adding it
directly to the ``pas`` package.


A simple example, the ``unreported`` subcommand
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A ``pas`` subcommand is built for each module found in the ``pas.commands``
package. For this operation to succeed, some conventions have to be respected;
suppose we want to add a new command to the pas utility (i.e. a command to list
all collected measures with no report), then we want to proceed as follows:

 1. Create a new python module inside the ``pas.commands`` package. Name it as
    you want to name your command. We want out command to be named
    ``unreported``, so we create the ``pas/commands/unreported.py`` file.
    
    **Note:** Filenames starting with underscores are automatically filtered
    out.
    
    If you run the ``pas`` utility, then an error is reported indicating that
    you don't have implemented the command correctly::
    
      $ pas unreported
           ERROR: No command found in module pas.commands.unreported
      usage: pas [-h] [--version] [-v] [-q] [--settings SETTINGS_MODULE]
               {authorize,execute,jobmgr,compile,init,measure} ...
      pas: error: invalid choice: 'unreported'

 2. To provide an implementation for a command, simply define a callable named
    ``command`` inside your ``unreported`` module. The callable shall accept
    one positional argument (which will be set to the command line options) and
    return a non-true value if the command succeeded::
    
      # Inside pas/commands/unreported.py
      
      def command(option):
         pass
    
    If you run the command now, it should exit cleanly without any message, but
    not much will be done. Let's write a simple implementation::
    
      import os
      import glob
      from pas.conf import settings

      def command(options):
          a = '{0}/*'.format(settings.paths['shared-measures'][0])
          r = '{0}/*/report'.format(settings.paths['shared-measures'][0])

          all_reports = set(glob.glob(a))
          already_reported = set([os.path.dirname(d) for d in glob.glob(r)])

          not_reported = all_reports - already_reported

          if not not_reported:
              print "No unreported measures found ({0} total measures)".format(
                      len(all_reports))
          elif len(not_reported) == 1:
              print "One unreported measure found ({0} total measures)".format(
                      len(all_reports))
          else:
              print "{0} unreported measures found ({1} total measures)".format(
                      len(not_reported), len(all_reports))

          for i, path in enumerate(not_reported):
              print "{0:2d}: {1}".format(i+1, os.path.basename(path))

 3. Suppose we want to allow the newly created subcommand to accept some
    optional (or required) flags and arguments; how can we add support for
    additional command line parsing to the current implementation?
    
    Fortunately the whole ``pas`` commands subsystem is based around the 
    `argparse <http://docs.python.org/dev/library/argparse.html>`_ module and
    adding options and arguments is straightforward. The ``pas`` command line
    parser builder looks if the module containing a command contains a
    callable named ``getparser`` and if it is the case it calls it passing the
    subcommand specific subparser instance to it.
    
    If we want to add a flag allowing to turn off the list of unreported
    measures (thus only showing the total counts), we can proceed as follows::
    
      import os
      import glob
      from pas.conf import settings

      def getparser(parser):
          parser.add_argument('-n', '--no-list', dest='show_list', default=True,
              action='store_false')

      def command(options):
          # [...]

          if options.show_list:
              for i, path in enumerate(not_reported):
                  print "{0:2d}: {1}".format(i+1, os.path.basename(path))

    Refer to the `argparse`_ documentation for the syntax and the usage of the
    module (just remember that the ``parser`` argument of the ``getparser``
    function is an ``ArgumentParser`` instance and the ``options`` argument
    passed to the command is a ``Namespace`` instance).

The example illustrated above covers the basics of creating a new subcommand
for the ``pas`` command line utility, but some more techniques allows to
achieve an higher degree of flexibility, naming :ref:`recursive subcommands`
and :ref:`external directory scanning`.


.. _recursive subcommands:
   
Recursive subcommands
---------------------

As stated in the introduction to the :ref:`architecture` section, the ``pas``
entry point *recursively* scans the ``pas.commands`` package for commands. This
allows to define ``pas`` subcommands which have themselves subcommands.

Take as an example the ``jobmgr`` subcommand. It defines different actions to 
be taken upon the different instances, such as ``start``, ``stop`` or ``kill``.
These three actions are defined as subcommands of the ``jobmgr`` subcommand.

To create a similar grouping structure for your commands collection, it
suffices to define your actions as modules inside a package named after the
collection name.

To reproduce a structure as the one implemented by the ``jobmgr`` command, the
following directory structure may be set up::

   + pas/
    \
     + commands/
      \
       + __init__.py
       + command1.py
       + command2.py
       |
       + jobmgr/
       |\
       | + __init__.py
       | + start.py
       | + stop.py
       | + kill.py
       |
       + command3.py

Then, you can invoke the ``jobmgr``'s ``start``, ``stop`` and ``kill``
subcommands simply by typing this command::

   $ pas jobmgr start

All other conventions (``command`` callable, ``getparser`` callable, argument
types,…) presented in the plain command example still hold for nested commands.


.. _external directory scanning:

External directory scanning
---------------------------

The main weak point of the architecture as it was presented until now is
certainly the fact that for the parser to recognize a new command, the command
itself has to be placed inside the ``pas.commands`` package.

Fortunately, a mechanism has been put in place to allow arbitrary directories
to be scanned for commands: the COMMAND_DIRECTORIES settings directive is a
list of directories to be scanned for commands *in addition* to the
``pas.commands`` package.

.. todo::
   Link to the settings documentation.

.. todo::
   Implement the retrieval of the directories to scan from the settings.

By adding your custom commands directory to the list you can have them
automatically included in the ``pas`` utility without the need to modify the
``pas`` source tree directly.

This is useful if you want to add some commands tied to a particular testing
environment or – if it is the case – to a particular :term:`measure case`.

.. note::
   You can override built-in commands simply by specifying a directory
   containing a command with the same name. Note although that **no recursive
   merge** is done, thus you can't override a single command of a commands
   collection while retaining all other collection subcommands.


.. _utilities:

Command utilities
-----------------

The ``pas.commands`` package provides some useful utilities to facilitate
common tasks when working with command definitions.

The API for these utilities is presented below. For each utility its use case
is described and a usage example is provided. To use them in your custom
commands definition simply import them from the ``pas.commands`` package.

Command decorators
~~~~~~~~~~~~~~~~~~

The following group of utilities can be used as decorators for the ``command``
callable:

.. autofunction:: pas.commands.nosettings
.. autofunction:: pas.commands.select_case
.. autofunction:: pas.commands.select_measure


Argument shortcuts
~~~~~~~~~~~~~~~~~~~

The following group of utilities can be used as factories for common/complex
additional arguments/option to bind to a parser instance for a custom
subcommand:

.. autofunction:: pas.commands.host_option
.. autofunction:: pas.commands.case_argument
.. autofunction:: pas.commands.measure_argument

