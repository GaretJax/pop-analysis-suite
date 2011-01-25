.. highlight:: bash

.. _quick-start:

Quick start
===========

The steps contained in this short guide should get you up and running in as few
steps as possible. For a full featured environment and for an in-dept
description of all the functionalities of the ``pas`` packages, refer to the
full documentation.

The following instructions assume that you have already installed the ``pas``
packages along with all its dependencies, if this is not the case, refer to the
:ref:`installation` instructions.

You don't need to understand completely what's going on in the following steps,
but the :ref:`execution-model` and the
:ref:`commands-reference` are a great resource to help you to grasp the details.


Step 1: Setup the test environment
----------------------------------

To run a measure, a test environment has to be setup. Fortunately this can
easily be done using the ``init`` command.

The init command tries to create a new environment in the current directory
(and will only succeed if it is empty) or using the path provided on the
command line. Use it in the following way::

   $ pas init <path-to-the-env>
   Attempting to create a new environment in '<path-to-the-env>'...
   Done.

If the command executed successfully, a newly created directory will be present
at the path you specified. Let's take a look at its content::

   $ ls -l <path-to-the-env>
   total 8
   -rw-r--r--   1 garetjax  staff  878 Jan 25 14:52 Vagrantfile
   drwxr-xr-x   4 garetjax  staff  136 Jan  3 21:30 cases
   drwxr-xr-x   6 garetjax  staff  204 Jan  4 00:00 conf
   drwxr-xr-x   4 garetjax  staff  136 Jan 12 21:51 contrib
   drwxr-xr-x   2 garetjax  staff   68 Jan  3 14:29 reports
   -rw-r--r--   1 garetjax  staff    0 Jan 25 14:52 settings.py

The entries in the listing have the following roles:

 * ``Vagrantfile``: Configuration file for the vagrant based virtual machine
   setup; already configured for a minimal master-slave setup.

 * ``cases``: Directory holding all measure cases which can be run in this
   environment. A ``simple`` test case is provided as an example.

 * ``conf``: Directory containing all environment specific configurations.
   Especially noteworthy is the ``chef`` subdirectory which holds the full VM
   configuration scripts. Also contained in this directory are the ``xsl``
   templates used for the measure simplification and report generation.

 * ``contrib``: Contributed assets and sourced to be used inside the
   environment. Already contained in this directory is a patched pop-c++
   version to avoid raw encoded communications.

 * ``reports``: The destination of all measure results along with the resulting
   reports.

 * ``settings.py``: An environment specific configuration file to allow to
   override system-wide settings directives.

.. note::

   For the remaining part of this quick-start we will assume that your current
   working directory corresponds to the environment root. If this is not yet
   the case, please ``cd <path-to-the-env>``.


Step 2: Setup the virtual machines
----------------------------------

Once the testing environment is created, the virtual machines on which the
measures will be run have to be created, booted and configured. Fortunately
this task is made simple by the ``vagrant`` tool::

   $ vagrant up

When you execute this command for the first time, the preconfigured virtual
machine box will be downloaded from the internet; in this case the following
text will be printed during the execution::
   
   [master] Provisioning enabled with Vagrant::Provisioners::ChefSolo...
   [master] Box lucid32 was not found. Fetching box from specified URL...
   [master] Downloading with Vagrant::Downloaders::HTTP...
   [master] Copying box to temporary location...
   Progress: 1% (5288808 / 502810112)

Once a machine is downloaded and booted, vagrant begins the "provisioning 
process", which simply means to copy the required chef recipes and resources
to the VM and to execute the set of defined actions to configure the host.

Once the complete process is finished, you have two running headless virtual
machines ready to execute pop-c services and objects.

You can play with them through ``ssh``. To connect simply issue::

   $ vagrant ssh master # s/master/slave/ if you want to connect to the slave instead


Step 3: Run the measure
-----------------------

In this quick-start we will run the base example bundled with the newly created
environment. Refer to the :ref:`measure-cases` document to get help on how to
create and personalize a new measure case.

The first thing to do when a new measure case is added to the library is to 
compile it on each virtual machine. To do so, issue the following command::

   $ pas compile

The ``compile`` subcommand asks you to choose the measure to compile (if there
is more than one choice) or, alternatively, you can provide the name of the
measure on the command line directly.

When run, the ``compile`` subcommand, automatically calls the default ``make``
target on each known host and makes sure to add the needed informations to a 
global ``obj.map`` file.

Once the sources are compiled, we are ready to run our measure. Measuring is
done through a ``tshark`` instance per host. ``pas`` provides commands to start
and stop ``tshark`` based measures on all or on selected hosts::

   $ pas measure start
   
   Only one test case found: simple.
   [33.33.33.10] sudo: rm -rf /measures ; mkdir /measures   
   [33.33.33.10] sudo: screen -dmS simple.lo.lo tshark -i lo -t e -w /measures/simple.lo.raw 'tcp and not tcp port 22'
   [33.33.33.10] sudo: screen -dmS simple.eth1.eth1 tshark -i eth1 -t e -w /measures/simple.eth1.raw 'tcp and not tcp port 22'
   [33.33.33.11] sudo: rm -rf /measures ; mkdir /measures
   [33.33.33.11] sudo: screen -dmS simple.lo.lo tshark -i lo -t e -w /measures/simple.lo.raw 'tcp and not tcp port 22'

The ``measure-start`` subcommand cleans up the measure destination directory on
the target-host and starts a detached named screen session to wrap the ``tshark``
process. This allows to let measures live between different connections and to
terminate them by name.

Now that the measure daemon is running, we can start the ``jobmgr`` and the
actual measure case.

.. note::

   If the initialization done by the ``jobmgr`` processes is not relevant for
   the measure, it is of course possible to start the job managers before
   starting the measure.

To start all job managers on all hosts -- and with some automatically provided
grace period -- issue the following command::

   $ pas jobmgr start

Finally we can also start the previously compiled pop binary and measure the
different established connections::

   $ pas execute

Once been through these different steps and having waited for the measured
program to terminated, the ``jobmgr``'s can be shut down and the measure
terminated. In short, this comes back to the following two commands::

   $ pas jobmgr stop ; pas measure stop

Congratulations, you just measured your first pop program using the POP
Analysis Suite, but the work is not over yet; all of the assets resulting from
the measure process are still dispersed all over your virtual machines. Head up
to the next section to learn how to assemble all the files into a readable
report.


Step 4: Generate the report
---------------------------

As anticipated above, all of the measures are still scattered over the
different virtual machines. The first step which has to be done to generate a 
report is to collect them in a unique place::

   $ pas measure collect

This command has the effect to gather all different measure files and place
them in an appropriate tree structure inside the ``report`` directory. The
different measures are first grouped by measure case + collection timestamp and
then by the IP of the originating virtual machine.

Once all files are collected, we can begin to process them::

   $ pas measure toxml     # Converts all measures to xml documents.

   $ pas measure simplify  # Simplifes the xml document by stripping
                           # unnecessary informations.

   $ pas measure decode    # Annotates the xml documents with the decoded
                           # POP Protocol payload.

The execution of these commands (the execution order is relevant) produces 3
new files for each ``<measure>.raw`` file:

 * A ``<measure>.xml`` file, containing the XML representation of the measure
   as returned by the ``tashark`` conversion command.

 * A ``<measure>.simple.xml`` file, containing the simplification of the
   previously converted measure. Only relevant data is preserved.

 * A ``<measure>.decoded.xml`` file, containing the same data of the simple XML
   version annotated with the decoded POP Protocol payload.

The final step allows to generated an HTML document containing the visual
representation of the full measure and some additional information. To launch
it run::

   $ pas measure report

To display the generated report in your browser, simply open the ``index.html``
file found in the ``reports/<case-name>_<timestamp>/report`` directory.

Wow, this was the final step! Sounds like a complicated and tedious process but
as you will see by reading the rest of the documentation, much of all this can
be automated, allowing to produce a complete report with a single command.

