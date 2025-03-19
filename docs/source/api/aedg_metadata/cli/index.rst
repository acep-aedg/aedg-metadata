aedg_metadata.cli
=================

.. py:module:: aedg_metadata.cli

.. autoapi-nested-parse::

   Entry point for metadata generating CLI



Attributes
----------

.. autoapisummary::

   aedg_metadata.cli.app


Functions
---------

.. autoapisummary::

   aedg_metadata.cli.hello


Module Contents
---------------

.. py:function:: hello(name: Annotated[str, typer.Argument(help='Last name of person to greet.')], count: Annotated[int, typer.Option(help='Number of times to repeat.')] = 1) -> None

   Simple program that greets NAME for a total of COUNT times.


.. py:data:: app
