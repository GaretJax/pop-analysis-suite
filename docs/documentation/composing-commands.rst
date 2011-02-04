.. _composed-commands:

Composing commands
==================

As you might have seen in the :ref:`quick-start`, running a measure from begin
to end is a process involving many different steps. If the environment has
already been set up and you are only tweaking your measure case source,
launching a whole measurement cycle requires more than 10 different commands.
Obviously, running them manually each time rapidly becomes cumbersome.

To solve exactly this problematic, ``pas`` introduced the concept of
*workflow*. A *workflow* is nothing else than a ``Makefile`` target invoked
trough the :mod:`pas run <pas.commands.run>` command.

The :mod:`pas run <pas.commands.run>` command simply takes care to invoke one
or more targets locally with the right environment variables set up and the
right working directory, as defined in the :ref:`make invocation` section.

Now that we know how to leverage the power of a ``make`` inside ``pas``, let's
take a look at a simple example. We want to be able to run a full measure
cycle, from compilation to reporting, with a single command.

This is the command we want to be able to execute::
   
   pas run <case-name> measureall

Then, the targets to add to the measure case specific ``Makefile`` to provide
the needed interface, would be the following:

.. code-block:: make

   measureall: compile measure report

   compile:
      pas compile $(MEASURE_NAME)
   
   measure:
      pas measure start
      pas jobmgr start
      pas execute $(MEASURE_NAME)
      pas jobmgr stop
      pas measure stop
      pas measure collect $(MEASURE_NAME)

   report:
      pas report toxml $(MEASURE_NAME)
      pas report simplify $(MEASURE_NAME)
      pas report decode $(MEASURE_NAME)
      pas report report $(MEASURE_NAME)

The ``Makefile`` of the bundled ``simple`` measure case already contains three
additional targets:

 * A ``run`` target to execute a measure by starting first the measure, then
   the job managers and in the end running the measure case by tearing it all
   down and collecting the data when finished.

 * A ``report`` target to generate the HTML report from the raw measures.
 
 * A ``reset`` target (inherited from the base ``Makefile``) which cleans all
   builds, kills all running measures and job managers and recompiles POP
   binaries from the sources for all hosts.

This commands composition technique allows us to automate some common workflows
and repetitive tasks. For more advanced commands which don't involve only
composition, the :ref:`custom commands <command-subsystem>` documentation
introduces the creation of commands using the very same tools as the ``pas``
subsytem.

