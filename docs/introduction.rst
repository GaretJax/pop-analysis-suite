.. highlight:: bash

Introduction
============

About
-----

The PAS package provides a command line utility and a measuring framework for
network analysis for the Parallel Object Programming protocol.

The tool allows to start POP-C++ nodes, run measure cases, capture the traffic
and produce a complete report of the exchanged TCP packets between the peers.

By default, the test infrastructure is set up using vagrant and some virtual
machines automatically configured using chef, but it is possible to use any
remote machine with ssh access and some configuration work (involving mainly
installing the needed dependencies and creating some shared folders).

Although this tool was developed especially for the C++ implementation of the
POP model, it was conceived to make as less assumptions as possible about the
underlying implementation and could easily be adapted to measure POP objects
offered by other implementations such, for example, as POP-Java

Further information about the POP-C++ project and the POP model can be found on
the `project's homepage <http://gridgroup.hefr.ch/popc/>`_.


Requirements
------------

The requirements necessary to install and run the ``pas`` utility are the
following:

 * Python >= 2.6 – http://python.org/;
 * ``vagrant`` and VirtualBox to run the virtual machines
   – http://vagrantup.com/;
 * A webkit based browser (Safari, Google Chrome,...) to display the reports.

The following libraries and utilities are optional but add some additional
features:

 * ``xmllint`` used to reformat the XML documents produced by the measures;
 * ``tidy`` used to cleanup the HTML output of the reports (note that the
   absence of this utility will add more entries to the list of unsupported
   browsers).

The Python packages that will automatically be installed by setuptools are the
following ones:

 * ``fabric`` to dispatch commands to remote machines through ssh
   – http://fabfile.org/;
 * ``pygments`` to highlight the source code and the decoded transactions
   – http://pygments.org/;
 * ``lxml`` to transform the different measure xml files
   – http://codespeak.net/lxml/.

.. _installation:

Installation
------------

Until a stable release is packaged and uploaded to the cheese shop, the latest
development snapshot can be installed directly from the github hosted sources
using ``easy_install`` or ``pip``::

   $ pip install https://github.com/GaretJax/pop-analysis-suite/tarball/master

.. note::
   Often, depending on the target system, the installation of a python package
   requires ``root`` privileges. If the previous command fails, retry to run it
   with ``sudo``.

To check if the package was correctly installed, run the the ``pas`` command on
the command line::

   $ pas

You should obtain an incorrect usage error similar to the following::

   usage: pas [-h] [--version] [-v] [-q] [--settings SETTINGS_MODULE]
              {authorize,execute,jobmgr,compile,init,measure} ...
   pas: error: too few arguments

Install from source
~~~~~~~~~~~~~~~~~~~

It is possible to install the PAs package directly from source. The following
commands should get you started::

   $ wget --no-check-certificate https://github.com/GaretJax/pop-analysis-suite/tarball/master
   $ tar -xzf GaretJax-pop-analysis-suite-*.tar.gz
   $ cd GaretJax-pop-analysis-suite-*
   $ python setup.py install


Setuptools
~~~~~~~~~~

To install the PAS package, the setuptools package is required (for both source
or remote installation modes). Albeit coming preinstalled on all major unix
based operating systems you may need to install it. 

You can obtain further information about ``setuptools`` either on its
`pypi project page <http://pypi.python.org/pypi/setuptools>`_ or on its
`official homepage <http://peak.telecommunity.com/DevCenter/setuptools>`_.


Development
-----------

The whole development of the PAS project happens on github, you can find the
source repository at the following address:
https://github.com/GaretJax/pop-analysis-suite/

Further development/contribution directives will be added as soon as some
interest is manifested by any hacker willing to participate in the development
process.


Structure of this manual
------------------------

This manual is conceived to offer an incremental approach to all feature which
the ``pas`` has to offer. It is structured in three main parts:

 1. The first part describes and documents the common usage of the tool, the
    assumptions it mades about different aspects such as VM setups, object
    communications, file locations and so on.
    
    Once read and understood this first part, a user should be able to complete
    a full measure cycle with a custom developed measure case and generate a
    report to further analyze.

 2. The second part dives in the internals of the ``pas`` libraries and
    documents topics such as command customization, custom type parsing or
    complex measurement setups, useful if a user want to completely adapt the
    offered functionalities to his needs.

 3. The third part contains reference documentation useful for both a basic or
    an advanced usage. There are references for all built-in commands, for the
    different settings directives or for more advanced topics such as the
    internal APIs.

This three parts are completed with this introduction, a glossary of common
terms and an alphabetical content index.


Building from source
~~~~~~~~~~~~~~~~~~~~

The present document is written using `Sphinx <http://sphinx.pocoo.org/>`_ and
it can either be `read online <http://readthedocs.org/docs/pas/>`_ thanks to
`readthedocs.org <http://readthedocs.org>`_ or built locally using the 
``sphinx`` tool into various different formats.

To create a local build, make sure to have the ``sphinx`` package installed and
run the following commands::

   $ git clone https://github.com/GaretJax/pop-analysis-suite/
   $ cd pop-analysis-suite/docs
   $ make html  # or any other format; run make without arguments to find out
                # the supported ones

The documentation builds will then be placed in the ``_build/<format>``
subdirectory.

