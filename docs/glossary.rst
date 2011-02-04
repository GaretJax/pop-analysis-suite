.. _glossary:


Glossary
========

.. glossary::
   :sorted:
   
   VM
   VMs
      The abbreviation for *virtual machine* and its plural form, respectively.
   
   PAS
   pas
      The abbreviation of *POP Analysis Suite*.
   
   virtual machine box
      A virtual machine box is a package containing a disk image with a
      preconfigured operating system on it. It can either already be present on
      the host system or automatically downloads from the internet when needed.
   
   CWD
      The abbreviation for *current working directory*.
   
   DSL
      The abbreviation for *Domain Specific Language*.
   
   POP
   POP model
      The abbreviation of *Parallel Object Programming* model.
   
   composer
   composers
      A function which allows to create complex or composite types using the
      :ref:`ppd-reference` syntax.

   complex type
   complex types
   composite type
   composite type
   compound type
   compound types
      Special data types for the POP Parsing DSL which are made up of different
      scalar or complex types.

   measure case
   measure cases
      A template for a measure. Contains source code, building instructions,
      measure workflow and optional commands to run and report the results of
      the measure case.

      :term:`test case` may be used as a synonym.

   test case
   test cases
      A synonym for :term:`measure case`

   testing environment
      A directory structure as set up by running the ``pas init`` command
      containing all the needed assets to run :term:`measure cases` and report
      results.
      
      A testing environment normally contains a set of custom virtual machines,
      some related :term:`measure cases`, environment specific settings and the
      results of the different :term:`measures`.

   role
      The role of a remote machine as seen by ``pas``. The default configuration
      defines and leverages the usage of a ``client`` role to run the POP
      application, a ``master`` role where the master ``jobmgr`` instance is run
      on and a ``slave`` role on which the slave ``jobmgr`` instances are run on.

   measure
   measures
      The results of a measure case which has been run.
      