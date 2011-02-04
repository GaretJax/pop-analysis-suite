.. _execution-model:

Execution model
===============

In the :ref:`quick-start` we have seen all steps needed to create an
environment, set up the virtual machines, run a measures and generate a report
from a practical point of view. In this document we will take a deeper look at
the inside workings of the pas tool and its execution model.

Once understood this model and acquired a good overview of the various commands
you will be ready to bend the ``pas`` utility to your will by simply combining
or adding different commands.

The following image will give you an high level overview of the execution model
of a measure in ``pas`` and the description of each step contains shortcuts to
relevant commands and configuration directive references:

.. image:: /assets/execution-model.*

The various steps of the execution model can best be described as follows:

 1. **Setup**
    
    This involves the initialization of the environment, the setup of the
    virtual machines and the creation of one or more measure cases.
    
    *Related commands:*
    :mod:`pas init <pas.commands.init>`,
    :mod:`pas authorize <pas.commands.authorize>`
    
    *Related settings:*
    :data:`VM_USER <pas.conf.basesettings.VM_USER>`,
    :data:`VM_PASSWORD <pas.conf.basesettings.VM_PASSWORD>`

 2. **Distribution and compilation**
    
    The first part of this step, the *distribution*, is automatically done by
    sharing the used directories between the host (your machine) and the guests
    (the virtual machines running on the host).
    
    The second part, the *compilation* is executed sequentially on each host
    and produces a binary build of the measure case for each different
    architecture in your VM setup.
    
    *Related commands:*
    :mod:`pas compile <pas.commands.compile>`
   
 3. **Beginning of the capturing process**
   
    A ``tshark`` instance is started on each configured interface of each guest
    and every filtered packet captured to a guest-local file.
    
    The ``tshark`` program is the command-line version of the well known
    `wireshark <http://wireshark.org>`_ network protocol analyzer.
    
    *Related commands:*
    :mod:`pas measure start <pas.commands.measure.start>`,
    :mod:`pas measure stop <pas.commands.measure.stop>`,
    :mod:`pas measure kill <pas.commands.measure.kill>`
    
    *Related settings:*
    :data:`CAPTURE_FILTER <pas.conf.basesettings.CAPTURE_FILTER>`, 
    :data:`INTERFACES <pas.conf.basesettings.INTERFACES>`

 4. **Job manager startup**
 
    A ``jobmgr`` is started on each guest, with a different configuration based
    on their role. The default setup defines a master and a slave role and the
    respective configuration to simulate the offloading of objects to a remote
    guest.
    
    *Related commands:*
    :mod:`pas jobmgr start <pas.commands.jobmgr.start>`,
    :mod:`pas jobmgr stop <pas.commands.jobmgr.stop>`,
    :mod:`pas jobmgr kill <pas.commands.jobmgr.kill>`
    
    *Related settings:*
    :data:`ROLES <pas.conf.basesettings.ROLES>`,
    :data:`STARTUP_DELAY <pas.conf.basesettings.STARTUP_DELAY>`,
    :data:`SHUTDOWN_DELAY <pas.conf.basesettings.SHUTDOWN_DELAY>`

 5. **POP program execution**
 
    The developed POP program is executed and the generated traffic captured by
    the different ``tshark`` processes.
   
    *Related commands:*
    :mod:`pas execute <pas.commands.execute>`
    
    *Related settings:*
    :data:`ROLES <pas.conf.basesettings.ROLES>`

 6. **Data collection**
 
    Once the POP program has executed and returned, the measure and the 
    job managers can be stopped.
    
    The results of each single measure and the different log files are now
    spread among all the different involved guests. The collection process
    retrieves all these files and copies them to a common shared location where
    the host can access them.
    
    *Related commands:*
    :mod:`pas measure collect <pas.commands.measure.collect>`
    
    *Related settings:*
    :data:`LOG_FILES <pas.conf.basesettings.LOG_FILES>`

 7. **Report generation**
 
    Now that the host has all measure results locally available it can process
    and assemble them into one or more measure reports.
    
    This process involves multiple steps, such as conversions, simplifications,
    payload decoding and the final assembly.  

    *Related commands:*
    :mod:`pas report toxml <pas.commands.report.toxml>`,
    :mod:`pas report simplify <pas.commands.report.simplify>`,
    :mod:`pas report decode <pas.commands.report.decode>`,
    :mod:`pas report report <pas.commands.report.report>`
    
    *Related settings:*
    :data:`DISPLAY_FILTER <pas.conf.basesettings.DISPLAY_FILTER>`

Once grasped these concepts you are ready to personalize your testing
environment. If you have not done so yet, hand over to the :ref:`quick-start`
for a step-by-step begin-to-end on how guide to take a measure or continue to
the detailed guide about how to :ref:`create measure cases <measure-cases>`.

The :ref:`advanced usage <advanced>` chapter provides documentation on more
technical and complicated aspected of the POP Analysis Suite needed to
completely customize and adapt an environment to special setups (i.e. a
preexisting setup with real machines).



