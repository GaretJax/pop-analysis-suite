.. _glossary:


Glossary
========

.. glossary::
   :sorted:

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

   measure
   measures
      The results of a measure case which has been run.