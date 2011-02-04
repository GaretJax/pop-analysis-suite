.. _ppd-reference:

POP Parsing DSL
===============

The informations transmitted in the POP encoded messages don't include the type
of the transmitted values as these are defined at compilation time and known to
both involved parties.

With the use of python and the need to decode message exchanges between
arbitrary peers, information about the transmitted values data-types is not
available and has to be provided somehow.

The implemented python based parser for POP messages introduces the concept of
a *types registry*. Each time a message has to be decoded, the specific types
of the payload are retrieved from the registry using the
``classid``/``methodid`` couple or the exception code contained in the POP
payload header.

As the measuring of arbitrary programs introduces new classes, methods and data
types, it does not suffice to provide a built-in set of known data types and
the need to let the final ``pas`` user specify custom and complex types arises.

For this purpose a special python-based domain specific language as been
defined. The DSL builds upon a few directives to be able to define primitive
types (rarely needed), complex types and new classes and to register them to
the registry in order to let the parser retrieve them when needed.

Refer to the :ref:`ppd-builtin` document for an overview of the already
provided types and classes.


Defining classes and methods
----------------------------

Defining a new class and its corresponding methods is an easy task thanks to
the declarative syntax offered by the POP Parsing DSL.

Each file which will finish up loaded by the types registry shares a common
import::

   from pas.parser.types import *

Once imported the different types, it is possible to use the
:func:`pas.parser.types.cls`, :func:`pas.parser.types.func` and
:func:`pas.parser.types.exc` functions to create new classes, methods and
exceptions respectively.

Their API is the following:

.. autofunction:: pas.parser.types.cls

.. autofunction:: pas.parser.types.func

.. autofunction:: pas.parser.types.exc

A possible definition of the ``paroc_service_base`` class using the parser DSL
is the following::

   # Import the POP types and the cls and func helpers
   from pas.parser.types import * 

   # Define the class and its methods
   cls(0, 'paroc_service_base', [
       func(0,  'BindStatus',  [],       [int, string, string]),   # broker_receive.cc:183
       func(1,  'AddRef',      [],       [int]),                   # broker_receive.cc:218
       func(2,  'DecRef',      [],       [int]),                   # broker_receive.cc:238
       func(3,  'Encoding',    [string], [bool]),                  # broker_receive.cc:260
       func(4,  'Kill',        [],       []),                      # broker_receive.cc:287
       func(5,  'ObjectAlive', [],       [bool]),                  # broker_receive.cc:302
       func(6,  'ObjectAlive', [],       []),                      # broker_receive.cc:319
       func(14, 'Stop',        [string], [bool]),                  # paroc_service_base.ph:47
   ])
   
   # Done. No further actions are required

By reading the preceding snippet, a few observations can be made:

 1. Not all methods are defined. In fact, the parser doesn't care if the object
    is fully defined or not until it doesn't receive a request or a response
    for an inexistent method ID.

 2. Methods can return multiple values. The first return value is always
    mapped to the C++ return value (if non-``void``), while the following
    values are mapped to the arguments which were passed as references.
 
 3. The ``bool`` type is often used in responses. The actual C++ return type is
    an ``int``, but as it is interpreted only as a success flag a ``bool``
    type has more semantic meaning in these particular cases.


Defining complex and composite types
------------------------------------

In the previous section the process of defining a new class and its methods was
presented, but the illustrated example was based on a relative simple class.

What has to be done, if for example, the ``POPCSearchNode`` class has to be
defined (more specifically its ``callbackResult`` method)?

The following is the signature of the ``POPCSearchNode::callbackResult``
method:

.. code-block:: cpp

   conc async void callbackResult(Response resp);

As you might have noticed, it takes a ``Response`` object as argument, so a
possible definition using the parser DSL syntax would be::

   cls(1001, 'POPCSearchNode', [
       # ...other methods here...
       func(38, 'callbackResult', [Response], []),
   ])
   
But how is the ``Response`` object defined and how does the parser know how to
decode it? The ``Response`` object is what in the python parser domain is
called a :term:`compound type` and fortunately its definition is much easier
than you might think; we know that a ``Response`` object is composed by a
``string``, a ``NodeInfo`` object and an ``ExplorationList`` object, so its
definition becomes::

   Response = compound('Response',
       ('uid', string),
       ('nodeInfo', NodeInfo),
       ('explorationList', ExplorationList),
   )

This example introduced two new concepts:

 1. The ``compound`` function, which allows to create composite objects based
    on a list of (``name``, ``type``) tuples;
 
 2. Nested compound objects definition. A compound object can further contain
    compound objects (the preceding snippet contains ``NodeInfo`` and
    ``ExplorationList`` as subtypes).

If we look deeper in detail, we'll see that the ``ExplorationList`` object
isn't actually a compound object, but rather a list of compound objects.

Fortunately, the task of defining a list is also easy using the shortcuts
offered by the DSL::

   ExplorationList = array(
       compound('ListNode',
           ('nodeId', string),
           ('visited', array(string)),
       )
   )

As you can see, defining new complex types is an easy task once the syntax and
the different :term:`composers` are known. Below you can find the API of the
different composers that come built-in with the python POP parser:

.. autofunction:: pas.parser.types.compound

.. autofunction:: pas.parser.types.dict

.. autofunction:: pas.parser.types.array

.. autofunction:: pas.parser.types.optional


Defining scalars
----------------

In the previous sections we have seen how to create new classes with bound
methods and how to define new argument or return types for those by combining
scalars into more complex structure in different ways.

The last building block needed to fully grasp the parsing details is the
decoding of scalars. It is here that the real work happens, as complex or
compound types only arrange scalars in different orders to decode a full
structure, but don't tell them *how* to decode the single values.

New scalar types are not needed as much as new complex types, but it can
serve to better understand the whole parsing process as well. Furthermore it
allows to define how to decode POP-C++ specific types (e.g. the
:c:type:`popbool` primitive) which don't comply with the standards.

A scalar type, as well as all types returned from the different composers seen
above, is simply a ``callable`` which accepts an `xdrlib.Unpacker`_ object
and returns a decoded python object. Refer to the ``Unpacker`` documentation
for further information about the already supported data types.

As an example, the implementation of the :c:type:`popbool` type is shown
below::

   import __builtin__

   # Define a callable which taks a single argument
   def popbool(stream):
      # Read an integer and check that the highest byte is set
      result = stream.unpack_int() & 0xff000000
      
      # Coearce the value to a boolean (use the __builtin__ pacakge as the
      # previous bool definition overwrote the built-in definition)
      return __builtin__.bool(result)

.. _xdrlib.Unpacker: http://docs.python.org/library/xdrlib.html#unpacker-objects








