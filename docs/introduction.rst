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
remote machine as soon as an ssh access is available and the required
dependencies installed.

.. todo::
   Add a section about usage without VMs.

Further information about the POP-C++ project and the POP model can be found on
the `project's homepage <http://gridgroup.hefr.ch/popc/>`_.


Requirements
------------

.. todo::
   Move the requirements and the installation subsections in a section on their
   own inside the documentation part.
   
.. todo::
   Add some simple instructions about setuptools and vagrant installation

The requirements necessary to install and run the ``pas`` utility are the
following:

 * Python 2.7 (although the whole package can easily be backported to Python
   2.6) – http://python.org/;
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

To check if the package was correctly installed, run the the ``pas`` command on
the command line::

   $ pas

You should obtain an incorrect usage error similar to the following::

   usage: pas [-h] [--version] [-v] [-q] [--settings SETTINGS_MODULE]
              {authorize,execute,jobmgr,compile,init,measure} ...
   pas: error: too few arguments

.. todo::
   Add note about sudo + package removal

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
or remote installation modes). You can obtain further information about
setuptools either on its
`pypi project page <http://pypi.python.org/pypi/setuptools>`_ or on
`the official homepage <http://peak.telecommunity.com/DevCenter/setuptools>`_.


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

.. todo::
   Describe the structure.

The present documentation is written using `Sphinx <http://sphinx.pocoo.org/>`_.

It can either be `read online <http://readthedocs.org/docs/pas/>`_ thanks to
`readthedocs.org <http://readthedocs.org>`_ or built locally using ``sphinx``.

To create a local build, make sure to have the ``sphinx`` package installed and
run the following commands::

   $ git clone https://github.com/GaretJax/pop-analysis-suite/
   $ cd pop-analysis-suite/docs
   $ make html  # or any other format; run make without arguments to find out
                # the supported ones

The documentation builds will then be placed in the ``_build/<format>``
subdirectory.

