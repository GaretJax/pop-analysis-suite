.. _advanced:

Advanced usage
==============

This section is intended for users which have already well understood the basic
concepts presented in the :ref:`first part <usage>` of the documentation and
are willing to customize a given testing environment to fulfill special needs.

By personalizing the environment using the directives presented in this
chapter, the ``pas`` tool as to be seen more as a framework for than as a
command line tool as the internals are much more exposed and it is possible
to interact directly with the basic building blocks of the same library used
by the built-in commands.

Four main arguments are presented in this chapter:

 1. The creation of subcommands allows to add arbitrary commands to the ``pas``
    utility by loading them from different locations and is described in the
    first section;
 
 2. The description of the python POP Parsing Domain Specific Language allows
    to create new complex types and defines classes to perform payload decoding
    of custom developed POP objects. This argument is treated in the second
    section;

 3. The third section introduces the assumptions the ``pas`` tool makes about
    the guest system and indicates therefore how a real machine has to be
    configured to being able to interact with the ``pas`` tool;

 4. By describing how to add and configure additional virtual machines, the
    understanding of the fourth section will let you create complex setups with
    different virtual machines and running measures on them.

.. toctree::

   command-subsystem
   ppd-reference
   real-machines
   vagrant
