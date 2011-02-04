.. _measure-cases:

Creating measure cases
======================

A :term:`measure case` in *PAS* is simply a directory containing a bunch of
special files. As we will see in this section, most of this structure is
based on a simple naming convention.

The default directory structure looks like the following::

   + <environment>/
    \
     + cases/
      \
       + <case-name-1>/
       |\
       | + Makefile
       | + src/
       | |\
       | | + source1.ph
       | | + source1.cc
       | | + main.cc
       | |
       | + types.py
       |
       + <case-name-2>/
       |\
       | + <...>
       |
       + <case-name-n>/
       
The only conventions which have to be respected for the measure case to
conform to the base model are the following:

 1. Each measure case shall be in its own directory inside the ``cases``
    subdirectory of the environment base directory;
    
 2. Each measure case shall contain a ``Makefile`` which shall provide some
    defined targets, see the :ref:`makefile` section);

 3. Each measure case shall contain a ``types.py`` file, defining all the types
    of the exchanged or called objects (see the :ref:`types` section).

The fact of placing your sources inside the ``src`` subdirectory is not
obligatory, but as described below, a base ``Makefile`` is provided and, to use
it, some more conventions have to be applied, it is thus better to respect this
rule too.


.. _makefile:

:file:`Makefile` targets
------------------------

As anticipated above, the measure case specific ``Makefile`` has to contain
some predefined targets to complain with the specification. These targets are
explained in greater detail in the next subsections.

To speed up the creation of a new measure case, a base makefile named
``Makefile.base`` is placed in the environment's ``conf`` directory. This file
can be included by the measure case specific ``Makefile`` to inherit the
already defined targets.

All required targets are already defined by the base makefile. If you are
option for the default build process and file organizations and don't need
exotic build configuration, including it should suffice to get you started.
Your measure case specific makefile will thus looks something like this:

.. code-block:: makefile
   
   include $(ENV_BASE)/conf/Makefile.base

.. note::
   The ``ENV_BASE`` variable contains the absolute path to the environment base
   directory and is automatically set to the correct value (either for local or
   remote invocation) by the ``pas`` command line tool.

The required targets (``build``, ``execute``, ``clean`` and ``cleanall``) are
further described below, along with their default implementation:

``build``
~~~~~~~~~

Is responsible to build the sources for the architecture on which it is
run on, by making sure that multiple builds of different architectures can
coexist at the same time. After each build, an ``obj.map`` file containing the
informations relative to *all* builds has also to be created or updated.

The exact location/naming of the produced artifacts is not standardized, as
they are needed only by the ``execute`` target.

The base ``Makefile`` provides this target by implementing it in the following
way:

.. code-block:: make

   SRCS=src/*.ph src/*.cc
   EXEC=$(notdir $(abspath .))
   ARCH=$$(uname -m)-$$(uname -p)-$$(uname -s)

   build: bin object

   dir:
   	mkdir -p build/$(ARCH)

   bin: dir
   	popcc -o $(EXEC) $(SRCS)
   	mv $(EXEC) build/$(ARCH)

   object: dir
   	popcc -object -o $(EXEC).obj $(SRCS)
   	mv $(EXEC).obj build/$(ARCH)
   	build/$(ARCH)/$(EXEC).obj -listlong >>build/obj.map
   	sort -u build/obj.map >build/obj.map.temp
   	mv build/obj.map.temp build/obj.map
   
``execute``
~~~~~~~~~~~

Allows to run an already built POP program on the architecture the target is
run on.
   
This target uses the artifacts produced by a run of the ``build`` target
(thus the binaries and the ``obj.map`` file) by choosing the correct
architecture; it has thus to be able to detect its architecture and to run the
respective binary.

The base makefile provides this target by implementing it in the following way:

.. code-block:: make

   EXEC=$(notdir $(abspath .))
   ARCH=$$(uname -m)-$$(uname -p)-$$(uname -s)

   execute:
      popcrun build/obj.map build/$(ARCH)/$(EXEC)

``clean``
~~~~~~~~~

Cleans up the compiled files for the architecture on which it is run on. As
before, this target is also already provided by the base makefile:

.. code-block:: make

   ARCH=$$(uname -m)-$$(uname -p)-$$(uname -s)

   clean:
      rm -rf *.o build/$(ARCH)

``cleanall``
~~~~~~~~~~~~

Cleans up all builds for all architectures for its measure case, simply
implemented as:

.. code-block:: make

   cleanall: clean
   	rm -rf build


.. _make invocation:

How will ``pas`` invoke make
----------------------------

As seen in the previous target definitions, the base ``Makefile`` makes
different assumptions about the ``CWD`` at invocation time and about some
variables which have to be set in the environment. To completely exploit all
features which ``make`` makes available, the details of the invocation have to
be known.

``pas`` differentiates between local (i.e. on the host machine) and remote
(i.e. on a guest or on a remote machine) invocations.

Remote invocations

   For remote invocations the path is set to the measure case base directory
   (i.e. a ``cd`` to ``ENV_BASE/cases/<case-name>`` is done).
   
   Additionally the ``ENV_BASE`` environment variable is set to the specific
   environment base location on the remote host as read from the :data1:`PATHS 
   <pas.conf.basesettings.PATHS>` settings directive.
   
   Remote invocations are executed by the :mod:`pas run <pas.commands.run>` and
   :mod:`pas execute <pas.commands.execute>` commands.

Local invocations

   For local invocations the path is left untouched, but both the
   ``ENV_BASE`` and ``EXEC`` environment variables are set and the ``-e`` flag
   passed to ``make`` in order to let environment variables override local
   defined variables.


.. _types:

Measure case specific types
---------------------------

It will often happen (if not always) that you create your custom POP-C++
classes for a specific measure case.

The python based parser used to decode the TCP payload cannot know what types
are encoded in it without further informations. To fulfill this need, custom
types can be created and registered to the parser using the
:ref:`ppd-reference`.

The :ref:`pas-report-decode` subcommand automatically loads the ``types.py``
file contained in the measure case directory and registers the contained types
for the decoding session.

.. note:
   If you don't defined any custom types, you can leave this file empty or
   delete it. The parser will automatically load the base types.

The syntax of this file is quite simple and based upon a declarative python
syntax; refer to the :ref:`ppd-reference` document for further information
about it and how to define your custom types.



