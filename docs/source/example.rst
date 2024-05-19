argparse\_typed Example
=======================

The ``argparse_typed`` package extends the buildin ``argparse`` package so that command line
parameters can be defined as a namespace class with PEP 484 type hints.
The members of the resulting namespace instance then have proper type hints attached.

Usage principle
---------------

Instead of instantiating an ``argparse.ArgumentParser`` and add arguments with the `add_argument()` method,
a new class is defined based on ``TypedNamespace`` with all attributes as class variables with type hints
and with ``argparse_typed.argument(...)`` as content. This class can then produce a suitable parser instance
using the ``parser()`` method or be passed to ``argparse_typed.TypedArgumentParser``.
Care is taken that the arguments have the name and type as stated by the class variable annotations.

The main benefit is the presence of type hints for all arguments.
An additional benefit is that the command line arguments are all defined cleanly in a single class scope.


This module supports all ``argparse`` features: adding arguments, groups, mutually exclusive groups and subparsers.
In general all `add_*` methods of ``argparse.ArgumentParser`` are defined by ``argparser_typed`` for usage in the
class definition but without the `add_` prefix.
Please also see the ``argparse`` documentation for the signature and usage.


Simple Example
--------------

Instead of the default ``argparse`` definition:

.. code-block:: python

        from argparse import ArgumentParser

        parser = ArgumentParser()
        parser.add_argument('-i', '--input')
        parser.add_argument('-o', '--output')
        parser.add_argument('-H', '--hex', action='store_true')
        parser.add_argument('-V', default=0.0)
        args = parser.parse_args()

resulting in an ``args`` Namespace without a good possibility to add type hints.
Therefore the IDE will not know which attributes ``args`` has or which type it should assume for them,
making static type checks impossible.

With ``argparse_typed`` the argument parser definition can be done using a class based on ``TypedNamespace``:

.. code-block:: python

        from argparse_typed import TypedArgumentParser, TypedNamespace, argument

        class Arguments(TypedNamespace):
            input: str = argument('-i', '--input')  # Variable name must match with long argument form
            output: str = argument('-o', '--output')
            hex: bool = argument('-H', '--hex', action='store_true')
            val: float = argument('-V', default=0.0)  # dest='val', type=float will be passed automatically

        parser = TypedArgumentParser[Arguments](namespacecls=Arguments)
        # or: parser = Arguments.parser()
        args: Arguments = parser.parse_args()

An IDE or other static type checker with PEP 484 support does now know that ``args`` has the
attributes `input`, `output`, `hex` and `val` with the given type hints.

Further Examples
----------------

Argument Groups:
...............

In order to add an arguments group use ``argument_group``.
Arguments can then be added to the group with its `argument()` method.

.. code-block:: python

        from argparse_typed import TypedNamespace, argument_group

        class Arguments(TypedNamespace):
            ungroupedarg = argument(...)
            ag = argument_group(title='Group title', description='Group descriptions')
            firstgroupedarg = ag.argument(...)
            secondgroupedarg = ag.argument(...)
            anotherungroupedarg = argument(...)
            ag2 = argument_group(title='Title of other group', description='Multiple groups possible')
            othergrouparg1 = ag2.argument(...)
            othergrouparg2 = ag2.argument(...)


Mutually Exclusive Groups:
..........................

In order to add a mutually exclusive group use ``mutually_exclusive_group``.
Arguments can then be added to the mutually exclusive group with its `argument()` method.


.. code-block:: python

        from argparse_typed import TypedNamespace, mutually_exclusive_group

        class Arguments(TypedNamespace):
            ungroupedarg = argument(...)
            meg = mutually_exclusive_group(title='Group title', description='Group descriptions')
            firstmutuallyexclusivearg = meg.argument(...)
            secondmutuallyexclusivearg = meg.argument(...)
            anotherungroupedarg = argument(...)


Subparsers:
...........

In order to add subparsers use ``subparsers`` to create a subparsers attachment and then add
the subparsers using `parser()`. Arguments to the subparsers can then be added with
the `argument()` method of the subparser instance.

.. code-block:: python

        from argparse_typed import TypedNamespace, subparsers

        class Arguments(TypedNamespace):
            sps = subparsers(title='Subcommands')
            subparser1 = sps.parser('foo', description='foo command')
            subparser2 = sps.parser('bar', description='bar command')

            bing: str = subparser1.argument('-B', '--bing')
            bang: str = subparser1.argument('-A', '--bang')
            blo: str = subparser2.argument('-O', '--blo')
            blu: str = subparser2.argument('-U', '--blu')


Clean namespace:
...............
If the scripts namespace should be kept clean from the several definition functions of ``argparse_typed``,
they can also be imported locally in the argument class:

.. code-block:: python

        from argparse_typed import TypedNamespace

        class Arguments(TypedNamespace):
            from argparse_typed import argument, argument_group
            somearg = argument(...)
            ag = argument_group()
            somegroupedarg = ag.argument(...)
            someothergroupedarg = ag.argument(...)

        args = Arguments.parser().parse_args()
