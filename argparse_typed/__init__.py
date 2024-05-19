"""Type hint support for argparse"""

import argparse
from typing import Any, Self, cast, Sequence, Literal, TypeAlias, Callable, Optional, Generic, TypeVar

# Type variable for generic namespaces
NS = TypeVar("NS", covariant=True, bound='TypedNamespace')

# Type aliases
ActionType: TypeAlias = Literal['store', 'store_const', 'store_true', 'store_false', 'append',
                                'append_const', 'count', 'help', 'version', 'extend']
NargsType: TypeAlias = int | Literal['?', '*', '+']

# Default argument to detect set keyword arguments
NONE: Any = object()


class _TypedNamespaceAttr:
    """Base class for attributes of a typed namespace class"""
    _impl: Any | None
    _parent: Optional['_TypedNamespaceAttr']

    def _set_impl(self, impl) -> Self:
        """Set implementation object."""
        self._impl = impl
        return self

    def _get_parent_impl(self, default: Any = None) -> Any:
        """Set implementation object of parent. Return default if not available."""
        try:
            return self._parent._impl                                               # type: ignore[union-attr]
        except AttributeError:
            return default

    def _set_parent(self, parent: '_TypedNamespaceAttr') -> Self:
        """Set parent."""
        self._parent = parent
        return self


class Argument(_TypedNamespaceAttr):
    """Represents a typed argument"""

    def __new__(cls, *args, **kwargs) -> Any:
        """Define return value as Any to allow arbitrary type hint on class variable."""
        return cast(Any, super().__new__(cls))

    def __init__(self,
                 *name_or_flags: Sequence[str],
                 action: ActionType | None = NONE,
                 nargs: NargsType | None = NONE,
                 const: Any | None = NONE,
                 default: Any | None = NONE,
                 type: Callable[[str], Any] | None = NONE,
                 choices: Sequence[Any] | None = NONE,
                 required: bool = NONE,
                 help: str | None = NONE,
                 metavar: str | None = NONE,
                 dest: str | None = NONE) -> None:
        """Command line argument definition.

            Args:
                *name_or_flags: A list of command-line option strings which should be associated with this action.
                action: String which specifies how an argument should be handled:
                        'store', 'store_const', 'store_true', 'append', 'append_const', 'count', 'help', 'version'.
                nargs: The number of command-line arguments that should be
                       consumed. By default, one argument will be consumed and a single
                       value will be produced.  Other values include:
                           - N (an integer) consumes N arguments (and produces a list)
                           - '?' consumes zero or one arguments
                           - '*' consumes zero or more arguments (and produces a list)
                           - '+' consumes one or more arguments (and produces a list)
                       Note that the difference between the default and nargs=1 is that
                       with the default, a single value will be produced, while with
                       nargs=1, a list containing a single value will be produced.
                const: The value to be produced if the option is specified and the
                       option uses an action that takes no values.
                default: The value to be produced if the option is not specified.
                type: A callable that accepts a single string argument, and
                      returns the converted value.  The standard Python types str, int,
                      float, and complex are useful examples of such callables.  If None,
                      str is used.
                choices: A container of values that should be allowed. If not None,
                         after a command-line argument has been converted to the appropriate
                         type, an exception will be raised if it is not a member of this
                         collection.
                required: True if the action must always be specified at the command line.
                          This is only meaningful for optional command-line arguments.
                help: The help string describing the argument.
                metavar: The name to be used for the option's argument with the help string.
                         If None, the 'dest' value will be used as the name.
                dest: The name of the attribute to hold the created object(s)
        """
        self.args = name_or_flags
        self.kwargs = {k: v for k, v in
                       dict(action=action, nargs=nargs, const=const, default=default, type=type, choices=choices,
                            required=required, help=help, metavar=metavar, dest=dest).items()
                       if v is not NONE}
        self._parent = None


class _TypedNamespaceAttrContainer(_TypedNamespaceAttr):
    """Base class for attributes of a typed namespace class which contain other attributes"""

    def argument(self,
                 *name_or_flags: Sequence[str],
                 action: ActionType | None = NONE,
                 nargs: NargsType | None = NONE,
                 const: Any | None = NONE,
                 default: Any | None = NONE,
                 type: Callable[[str], Any] | None = NONE,
                 choices: Sequence[Any] | None = NONE,
                 required: bool = NONE,
                 help: str | None = NONE,
                 metavar: str | None = NONE,
                 dest: str | None = NONE) -> Any:
        """Command line argument definition.

            Args:
                *name_or_flags: A list of command-line option strings which should be associated with this action.
                action: String which specifies how an argument should be handled:
                        'store', 'store_const', 'store_true', 'append', 'append_const', 'count', 'help', 'version'.
                nargs: The number of command-line arguments that should be
                       consumed. By default, one argument will be consumed and a single
                       value will be produced.  Other values include:
                           - N (an integer) consumes N arguments (and produces a list)
                           - '?' consumes zero or one arguments
                           - '*' consumes zero or more arguments (and produces a list)
                           - '+' consumes one or more arguments (and produces a list)
                       Note that the difference between the default and nargs=1 is that
                       with the default, a single value will be produced, while with
                       nargs=1, a list containing a single value will be produced.
                const: The value to be produced if the option is specified and the
                       option uses an action that takes no values.
                default: The value to be produced if the option is not specified.
                type: A callable that accepts a single string argument, and
                      returns the converted value.  The standard Python types str, int,
                      float, and complex are useful examples of such callables.  If None,
                      str is used.
                choices: A container of values that should be allowed. If not None,
                         after a command-line argument has been converted to the appropriate
                         type, an exception will be raised if it is not a member of this
                         collection.
                required: True if the action must always be specified at the command line.
                          This is only meaningful for optional command-line arguments.
                help: The help string describing the argument.
                metavar: The name to be used for the option's argument with the help string.
                         If None, the 'dest' value will be used as the name.
                dest: The name of the attribute to hold the created object(s)

            Returns:
                An Argument instance but as type Any so that variable can be typed with the actual type.
        """
        return Argument(*name_or_flags, action=action, nargs=nargs, const=const,
                        default=default, type=type, choices=choices, required=required,
                        help=help, metavar=metavar, dest=dest)._set_parent(self)


class ArgumentGroup(_TypedNamespaceAttrContainer):
    """Represents an argument group.

       Args:
            title (str): Optional title of the group.
            description (str): Optional description of the group.
    """

    def __init__(self, title: str | None = None, description: str | None = None) -> None:
        self.title = title
        self.description = description
        self._parent = None
        self._impl = None


class MutuallyExclusiveGroup(ArgumentGroup):
    """Represents a mutually exclusive group.
       Additionally to the add_mutually_exclusive_group() parameter 'required' it also accepts the parameters of
       add_argument_group() 'title' and 'description'. If any of these two are set the mutually exclusive group
       is added to an argument group with these parameters, otherwise directly to the parser.

       Args:
            required (bool): If true one argument of this group must be provided.
            title (str): Optional title of the group.
            description (str): Optional description of the group.
    """

    def __init__(self, required: bool = False, title: str | None = None, description: str | None = None) -> None:
        self.required = required
        super().__init__(title, description)


class _Subparser(_TypedNamespaceAttrContainer):
    """Representation of a subparser"""

    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs
        self._parent = None
        self._impl = None


class Subparsers(_TypedNamespaceAttr):
    """Representation of a subparsers element of argparse."""

    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs
        self._parent = None
        self._impl = None

    def parser(self, *args, **kwargs) -> _Subparser:
        """Add a subparser to the subparsers collection."""
        return _Subparser(*args, **kwargs)._set_parent(self)


class TypedArgumentParser(argparse.ArgumentParser, Generic[NS]):

    def __init__(self,
                 *,
                 prog: str | None = None,
                 usage: str | None = None,
                 description: str | None = None,
                 epilog: str | None = None,
                 parents: Sequence[argparse.ArgumentParser] = (),
                 formatter_class: type[argparse.HelpFormatter] = argparse.HelpFormatter,
                 prefix_chars: str = '-',
                 fromfile_prefix_chars: str | None = None,
                 argument_default: Any | None = None,
                 conflict_handler: str = 'error',
                 add_help: bool = True,
                 allow_abbrev: bool = True,
                 exit_on_error: bool = True,
                 namespacecls: type[NS] | None = None):
        """
        ArgumentParser with type hint support. Can create arguments from typed namespace class.

        Args:
            prog: The name of the program (default: os.path.basename(sys.argv[0]))
            usage: The string describing the program usage (default: generated from arguments added to parser)
            description: Text to display before the argument help (by default, no text)
            epilog: Text to display after the argument help (by default, no text)
            parents: A list of ArgumentParser objects whose arguments should also be included
            formatter_class: A class for customizing the help output
            prefix_chars: The set of characters that prefix optional arguments (default: '-')
            fromfile_prefix_chars: The set of characters that prefix files from which additional arguments
                                   should be read (default: None)
            argument_default: The global default value for arguments (default: None)
            conflict_handler: The strategy for resolving conflicting optionals (usually unnecessary)
            add_help: Add a -h/--help option to the parser (default: True)
            allow_abbrev: Allows long options to be abbreviated if the abbreviation is unambiguous. (default: True)
            exit_on_error: Determines whether or not ArgumentParser exits with error info when an error occurs.
                           (default: True)
            namespacecls: TypedNamespace class with argument definitions for the parser.
        """
        self.namespacecls = namespacecls
        super().__init__(prog, usage, description, epilog, parents, formatter_class, prefix_chars,
                         fromfile_prefix_chars, argument_default, conflict_handler, add_help,
                         allow_abbrev, exit_on_error)
        if namespacecls is not None:
            self.add_arguments_from_namespace(namespacecls)

    def add_arguments_from_namespace(self: argparse.ArgumentParser,
                                     namespacecls: type[argparse.Namespace]) -> argparse.ArgumentParser:
        """Add arguments from typed namespace class."""
        for attrname, attr in getattr(namespacecls, '_argparse_typed', vars(namespacecls)).items():
            if not attrname.startswith('_'):  # Ignore attributes starting with underscore
                # Handle according to type
                if isinstance(attr, MutuallyExclusiveGroup):
                    # If a title or description is set we need to wrap it into an argument group first
                    if attr.title is not None or attr.description is not None:
                        group = self.add_argument_group(attr.title, attr.description).add_mutually_exclusive_group(
                            required=attr.required)
                    else:
                        group = self.add_mutually_exclusive_group(required=attr.required)
                    attr._set_impl(group)

                elif isinstance(attr, ArgumentGroup):
                    # If an ArgumentGroup add a new argument group to the parser and connect it to the attribute
                    attr._set_impl(self.add_argument_group(attr.title, attr.description))

                elif isinstance(attr, Argument):
                    # Do same checks as argparse to avoid problems in add_argument() later.
                    if len(attr.args) == 1 and attr.args[0][0] not in self.prefix_chars:
                        # Single positional argument must match name of attribute
                        if attr.args[0] != attrname:
                            raise ValueError(
                                f'Single position argument "{attr.args[0]}" must match attribute name "{attrname}"')
                    else:
                        # If destination is not given use attribute name
                        dest = attr.kwargs.setdefault('dest', attrname)
                        # If given then it must match attribute name
                        if dest != attrname:
                            raise ValueError(
                                f'Keyword argument "dest": "{dest}" must match attribute name "{attrname}"')
                    try:
                        # Set type from annotated type if not already set and action is compatible
                        action: ActionType | None = attr.kwargs.get('action')                 # type: ignore[assignment]
                        if action is None or not action.startswith('store_'):
                            attr.kwargs.setdefault('type', namespacecls.__annotations__[attrname])
                    except (AttributeError, KeyError):
                        # Ignore missing annotated type
                        pass

                    # Finally add argparse argument to attribute parent (group, subparser or this parser)
                    attr._get_parent_impl(default=self).add_argument(*attr.args, **attr.kwargs)

                elif isinstance(attr, Subparsers):
                    # Add subparsers to parser, set as implementation of Subparsers instance
                    attr._set_impl(self.add_subparsers(*attr.args, **attr.kwargs))

                elif isinstance(attr, _Subparser):
                    # Add new subparser to subparsers (i.e. the implementation of the parent)
                    attr._set_impl(attr._get_parent_impl().add_parser(*attr.args, **attr.kwargs))
        return self

    def parse_args(self, args: Sequence[str] | None = None,                                     # type: ignore[override]
                   namespace: argparse.Namespace | None = None) -> NS:
        """Parse arguments."""
        if namespace is None and self.namespacecls is not None:
            namespace = self.namespacecls()
        return cast(NS, super().parse_args(args, namespace))

    def parse_known_args(self, args: Sequence[str] | None = None,                               # type: ignore[override]
                         namespace: argparse.Namespace | None = None) -> tuple[NS, list[str]]:
        """Parse known arguments."""
        if namespace is None and self.namespacecls is not None:
            namespace = self.namespacecls()
        return cast(tuple[NS, list[str]], super().parse_known_args(args, namespace))

    def parse_intermixed_args(self, args: Sequence[str] | None = None,                          # type: ignore[override]
                              namespace: argparse.Namespace | None = None) -> NS:
        """Parse intermixed arguments."""
        if namespace is None and self.namespacecls is not None:
            namespace = self.namespacecls()
        return cast(NS, super().parse_intermixed_args(args, namespace))

    def parse_known_intermixed_args(self, args: Sequence[str] | None = None,                    # type: ignore[override]
                                    namespace: argparse.Namespace | None = None) -> tuple[NS, list[str]]:
        """Parse known intermixed arguments."""
        if namespace is None and self.namespacecls is not None:
            namespace = self.namespacecls()
        return cast(tuple[NS, list[str]], super().parse_known_intermixed_args(args, namespace))


class TypedNamespaceMeta(type):
    """Metaclass for TypedNamespace.
       Will move all public class attributes to a private dictionary to avoid name clashes between
       the argument definition as class attribute and the resulting parsed argument as instance attribute.
    """

    def __new__(cls, name: str, bases: tuple[type, ...], dct: dict[str, Any]):
        """Produce new TypedNamespace class."""
        # Move class variables into private dictionary
        arguments = {}
        for key, value in list(dct.items()):
            if not key.startswith('_') and isinstance(value, _TypedNamespaceAttr):
                arguments[key] = dct.pop(key)
        dct['_argparse_typed'] = arguments

        return super().__new__(cls, name, bases, dct)


class TypedNamespace(argparse.Namespace, metaclass=TypedNamespaceMeta):
    """Base class for Namespace with type hints"""

    @classmethod
    def parser(cls, *args, **kwargs) -> TypedArgumentParser[Self]:
        """Return an argument parser instance for arguments defined by this typed namespace class"""
        return TypedArgumentParser[Self](*args, **kwargs, namespacecls=cls)


def argument(*name_or_flags: Sequence[str],
             action: ActionType | None = NONE,
             nargs: NargsType | None = NONE,
             const: Any | None = NONE,
             default: Any | None = NONE,
             type: Callable[[str], Any] | None = NONE,
             choices: Sequence[Any] | None = NONE,
             required: bool = NONE,
             help: str | None = NONE,
             metavar: str | None = NONE,
             dest: str | None = NONE) -> Any:
    """Command line argument definition.

        Args:
            *name_or_flags: A list of command-line option strings which should be associated with this action.
            action: String which specifies how an argument should be handled:
                    'store', 'store_const', 'store_true', 'append', 'append_const', 'count', 'help', 'version'.
            nargs: The number of command-line arguments that should be
                   consumed. By default, one argument will be consumed and a single
                   value will be produced.  Other values include:
                       - N (an integer) consumes N arguments (and produces a list)
                       - '?' consumes zero or one arguments
                       - '*' consumes zero or more arguments (and produces a list)
                       - '+' consumes one or more arguments (and produces a list)
                   Note that the difference between the default and nargs=1 is that
                   with the default, a single value will be produced, while with
                   nargs=1, a list containing a single value will be produced.
            const: The value to be produced if the option is specified and the
                   option uses an action that takes no values.
            default: The value to be produced if the option is not specified.
            type: A callable that accepts a single string argument, and
                  returns the converted value.  The standard Python types str, int,
                  float, and complex are useful examples of such callables.  If None,
                  str is used.
            choices: A container of values that should be allowed. If not None,
                     after a command-line argument has been converted to the appropriate
                     type, an exception will be raised if it is not a member of this
                     collection.
            required: True if the action must always be specified at the command line.
                      This is only meaningful for optional command-line arguments.
            help: The help string describing the argument.
            metavar: The name to be used for the option's argument with the help string.
                     If None, the 'dest' value will be used as the name.
            dest: The name of the attribute to hold the created object(s)

        Returns:
            An Argument instance but as type Any so that variable can be typed with the actual type.
    """
    return Argument(*name_or_flags, action=action, nargs=nargs, const=const, default=default, type=type,
                    choices=choices, required=required, help=help, metavar=metavar, dest=dest)


def argument_group(title: str | None = None, description: str | None = None) -> ArgumentGroup:
    """Returns an ArgumentGroup instance. This wrapper is only for naming consistency.

    Args:
        title (str): Optional title of the group.
        description (str): Optional description of the group.

    Returns:
        ArgumentGroup instance
    """
    return ArgumentGroup(title=title, description=description)


def mutually_exclusive_group(required=False, title=None, description=None) -> MutuallyExclusiveGroup:
    """Returns an MutuallyExclusiveGroup instance. This wrapper is only for naming consistency.

    Args:
        required (bool): If true one argument of this group must be provided.
        title (str): Optional title of the group.
        description (str): Optional description of the group.

    Returns:
        MutuallyExclusiveGroup instance
    """
    return MutuallyExclusiveGroup(required=required, title=title, description=description)


def subparsers(*args, **kwargs) -> Subparsers:
    """Returns a Subparsers instance. This wrapper is only for naming consistency."""
    return Subparsers(*args, **kwargs)


def add_arguments_from_namespace(parser: argparse.ArgumentParser,
                                 namespacecls: type[argparse.Namespace]) -> argparse.ArgumentParser:
    """Add (more) arguments from typed namespace class to ArgumentParser."""
    return TypedArgumentParser.add_arguments_from_namespace(parser, namespacecls)


__all__ = ['argument', 'argument_group', 'mutually_exclusive_group', 'subparsers',
           'add_arguments_from_namespace',
           'TypedNamespace', 'TypedArgumentParser']
