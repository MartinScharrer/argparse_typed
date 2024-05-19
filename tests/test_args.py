import argparse
import itertools

from argparse import ArgumentParser
from argparse_typed import TypedNamespace, TypedArgumentParser, Argument, subparsers, argument, \
                           argument_group, mutually_exclusive_group, add_arguments_from_namespace
from unittest import TestCase


class TestArgs(TestCase):

    def test_args(self) -> None:
        class Arguments(TypedNamespace):
            input: str = argument('-i', '--input')
            output: str = argument('-o', '--output')
            hex: bool = argument('-H', '--hex', action='store_true')
            val: float = argument('-V', default=0.0)
        args: Arguments = TypedArgumentParser[Arguments](namespacecls=Arguments).parse_args(['-i', 'abc', '-o', 'def', '-H'])
        self.assertEqual(args.input, 'abc')
        self.assertEqual(args.output, 'def')
        self.assertTrue (args.hex)
        self.assertEqual(args.val, 0.0)
        self.assertIsInstance(args, Arguments)

    def test_args_dest_ok(self) -> None:
        class Arguments(TypedNamespace):
            testname1: str = argument('--testname1')
            testname2: str = argument('--othername2')  # dest='testname1' automatically added
            testname3: str = argument('--othername3', dest='testname3')  # explicit dest valid if identical
        args = Arguments.parser().parse_args(['--testname1', 'testvalue1',
                                              '--othername2', 'testvalue2',
                                              '--othername3', 'testvalue3'])
        self.assertEqual(args.testname1, 'testvalue1')
        self.assertEqual(args.testname2, 'testvalue2')
        self.assertEqual(args.testname3, 'testvalue3')
        self.assertIsInstance(args, Arguments)

    def test_args_dest_failed(self) -> None:
        class Arguments(TypedNamespace):
            testname: str = argument('--othername', dest='othername')
        with self.assertRaises(ValueError):
            Arguments.parser()

    def test_args_positional_failed(self) -> None:
        class Arguments(TypedNamespace):
            testname: str = argument('othername')
        with self.assertRaises(ValueError):
            Arguments.parser()

    def test_args_positional_failed2(self) -> None:
        class Arguments(TypedNamespace):
            testname: str = argument('othername', dest='testname')
        with self.assertRaises(ValueError):
            Arguments.parser()

    def test_add_namespace(self) -> None:
        class Arguments(TypedNamespace):
            input: str = argument('-i', '--input')
            output: str = argument('-o', '--output')
            hex: bool = argument('-H', '--hex', action='store_true')
            val: float = argument('-V', default=0.0)

        for parsercls in (ArgumentParser, TypedArgumentParser):
            with self.subTest(parsercls=parsercls):
                parser = parsercls()
                add_arguments_from_namespace(parser, Arguments)
                args: Arguments = parser.parse_args(['-i', 'abc', '-o', 'def', '-H'])
                self.assertEqual(args.input, 'abc')
                self.assertEqual(args.output, 'def')
                self.assertTrue (args.hex)
                self.assertEqual(args.val, 0.0)

    def test_subparsers(self) -> None:
        class Arguments(TypedNamespace):
            sps = subparsers(title='Subcommands')
            subparser1 = sps.parser('foo', description='foo command')
            subparser2 = sps.parser('bar', description='bar command')

            bing: str = subparser1.argument('-B', '--bing')
            bang: str = subparser1.argument('-A', '--bang')
            blo: str = subparser2.argument('-O', '--blo')
            blu: str = subparser2.argument('-U', '--blu')
        arg_parser = TypedArgumentParser[Arguments](namespacecls=Arguments)
        with self.assertRaises(SystemExit):
            arg_parser.parse_args(['-h'])
        with self.assertRaises(SystemExit):
            arg_parser.parse_args(['foo', '-h'])
        with self.assertRaises(SystemExit):
            arg_parser.parse_args(['bar', '-h'])

    def test_subparsers2(self) -> None:
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(title='Subcommands')
        subparser1 = subparsers.add_parser('foo')
        subparser1.add_argument('-B', '--bing')
        subparser1.add_argument('-A', '--bang')
        with self.assertRaises(SystemExit):
            parser.parse_args(['-h'])

    def test_3(self) -> None:
        class Arguments(TypedNamespace):

            @staticmethod
            def hexint(s: str) -> int:
                return int(s, 16)

            filename: str = argument('filename')
            output: float = argument('-o', '--output', action='store')
            hex: bool = argument('-H', '--hex', action='store_true', dest='hex')
            hi: int = argument('-I', type=hexint)

            group1 = mutually_exclusive_group(required=True, title='Bla', description='Some blalallala')
            test1: bool = group1.argument('-E', action='store_true')
            test2: bool = group1.argument('-R', action='store_true')
            test3: bool = group1.argument('-T', action='store_true')

        parser = TypedArgumentParser[Arguments](prog='Test Application',
                                                description='Test for ArgumentParserWithTypes',
                                                namespacecls=Arguments)
        args: Arguments = parser.parse_args(['testfilename', '-o', '11.2', '--hex', '-I', '1234A', '-E'])

        x = (args.filename, args.output, args.hex, args.hi, args.test1)
        with self.assertRaises(SystemExit):
            parser.parse_args(['-h'])

    def test_4(self) -> None:
        class Arguments(TypedNamespace):
            a: str = argument('-a')
            b: int = argument('-b')

        parser = Arguments.parser(prog='Test Application', description='Test for ArgumentParserWithTypes')
        args = parser.parse_args([])
        self.assertIsInstance(args, Arguments)

    def test_argument_empty(self) -> None:
        class Arguments(TypedNamespace):
            pass
        parser = TypedArgumentParser[Arguments](namespacecls=Arguments)
        with self.assertRaises(SystemExit):
            a = parser.parse_args(['-h'])
        parser2 = TypedArgumentParser().add_arguments_from_namespace(Arguments)
        with self.assertRaises(SystemExit):
            parser2.parse_args(['-h'])

    def test_argument_group(self) -> None:
        class Arguments(TypedNamespace):
            ag0 = argument_group()
            ag1 = argument_group('Test 1')
            ag2 = argument_group('Test 2', 'Test it 2')
            ag3 = argument_group(title='Test 3', description='Test it 3')
            ag4 = argument_group(title='Test 4', description='Test it 4')
            ag5 = argument_group(title='Test 5')
            ag6 = argument_group(description='Test it 6')
            ag7 = argument_group(title='Test 7', description='Test it 7')
            ag8 = argument_group(title='Test 8')
            ag9 = argument_group(description='Test it 9')
        parser = TypedArgumentParser(prog='test_argument_group', namespacecls=Arguments)
        with self.assertRaises(SystemExit):
            parser.parse_args(['-h'])


    def test_mutually_exclusive_group(self) -> None:
        class Arguments(TypedNamespace):
            meg = mutually_exclusive_group(required=True, title='Bla', description='Some blalallala')
            test1: bool = meg.argument('-E', action='store_true')
            test2: bool = meg.argument('-R', action='store_true')
            test3: bool = meg.argument('-T', action='store_true')

        parser = TypedArgumentParser[Arguments](prog='Test Application',
                                                description='Test for ArgumentParserWithTypes',
                                                namespacecls=Arguments)
        TESTFLAGS = ('-E', '-R', '-T')
        # Test if OK when only one is used
        for testflag in TESTFLAGS:
            with self.subTest(testflag):
                args: Arguments = parser.parse_args([testflag])
                self.assertEqual(args.test1, testflag == '-E')
                self.assertEqual(args.test2, testflag == '-R')
                self.assertEqual(args.test3, testflag == '-T')

        # Test if not OK when used two
        for testflags in itertools.combinations(TESTFLAGS, 2):
            with self.subTest(testflags), self.assertRaises(SystemExit):
                args: Arguments = parser.parse_args([*testflags])

        # Test if not OK when used all three
        with self.subTest(TESTFLAGS), self.assertRaises(SystemExit):
            parser.parse_args([*TESTFLAGS])

        # Test if really required
        with self.subTest('required'), self.assertRaises(SystemExit):
            parser.parse_args([])

    def test_mutually_exclusive_group_not_requried(self) -> None:
        class Arguments(TypedNamespace):
            meg = mutually_exclusive_group(required=False)
            test1: bool = meg.argument('-E', action='store_true')
            test2: bool = meg.argument('-R', action='store_true')
            test3: bool = meg.argument('-T', action='store_true')

        parser = TypedArgumentParser[Arguments](prog='Test Application',
                                                description='Test for ArgumentParserWithTypes',
                                                namespacecls=Arguments)

        args = parser.parse_args([])
        self.assertFalse(args.test1)
        self.assertFalse(args.test2)
        self.assertFalse(args.test3)
        self.assertIsInstance(args, Arguments)

    def test_arg_type_annotated(self) -> None:
        class Arguments(TypedNamespace):
            testname: str = argument('--testname', type=str)
        args = Arguments.parser().parse_args(['--testname', 'testvalue'])
        self.assertEqual(args.testname, 'testvalue')
        self.assertIsInstance(args, Arguments)

    def test_arg_type_not_annotated(self) -> None:
        class Arguments(TypedNamespace):
            testname = argument('--testname', type=str)
        args = Arguments.parser().parse_args(['--testname', 'testvalue'])
        self.assertEqual(args.testname, 'testvalue')
        self.assertIsInstance(args, Arguments)

    def test_arg_type_annotation_mismatch(self) -> None:
        """Permitted: argument is type annotated differently than the type parameter.
           The paramter might be a function not a class/type but return the annotated type.
        """
        class Arguments(TypedNamespace):
            testname: int = argument('--testname', type=str)
        args = Arguments.parser().parse_args(['--testname', 'testvalue'])
        self.assertEqual(args.testname, 'testvalue')
        self.assertIsInstance(args, Arguments)

    def test_parse_args(self) -> None:
        class Arguments(TypedNamespace):
            testname: str = argument('--testname')
        args = Arguments.parser().parse_args(['--testname', 'testvalue'])
        self.assertEqual(args.testname, 'testvalue')
        self.assertIsInstance(args, Arguments)

    def test_parse_args_no_ns(self) -> None:
        parser = TypedArgumentParser()
        parser.add_argument('--testname')
        args = parser.parse_args(['--testname', 'testvalue'])
        self.assertEqual(args.testname, 'testvalue')
        self.assertIsInstance(args, argparse.Namespace)

    def test_parse_args_extra_ns(self) -> None:
        class Arguments(argparse.Namespace):
            testname: str
        parser = TypedArgumentParser()
        parser.add_argument('--testname')
        args: Arguments = parser.parse_args(['--testname', 'testvalue'], Arguments())
        self.assertEqual(args.testname, 'testvalue')
        self.assertIsInstance(args, Arguments)

    def test_parse_known_args(self) -> None:
        class Arguments(TypedNamespace):
            testname: str = argument('--testname')
        args, rest = Arguments.parser().parse_known_args(['--testname', 'testvalue', '-a', '--bla', 'test'])
        self.assertEqual(args.testname, 'testvalue')
        self.assertSequenceEqual(rest, ['-a', '--bla', 'test'])
        self.assertIsInstance(args, Arguments)

    def test_parse_known_args_no_ns(self) -> None:
        parser = TypedArgumentParser()
        parser.add_argument('--testname')
        args, rest = parser.parse_known_args(['--testname', 'testvalue', '-a', '--bla', 'test'])
        self.assertEqual(args.testname, 'testvalue')
        self.assertSequenceEqual(rest, ['-a', '--bla', 'test'])
        self.assertIsInstance(args, argparse.Namespace)

    def test_parse_known_args_extra_ns(self) -> None:
        class Arguments(argparse.Namespace):
            testname: str
        parser = TypedArgumentParser()
        parser.add_argument('--testname')
        args, rest = parser.parse_known_args(['--testname', 'testvalue', '-a', '--bla', 'test'], Arguments())
        self.assertEqual(args.testname, 'testvalue')
        self.assertSequenceEqual(rest, ['-a', '--bla', 'test'])
        self.assertIsInstance(args, Arguments)

    def test_parse_intermixed_args(self) -> None:
        class Arguments(TypedNamespace):
            foo: str = argument('--foo')
            cmd: str = argument('cmd')
            rest: list[int] = argument('rest', nargs='*', type=int)
        args = Arguments.parser().parse_intermixed_args('doit 1 --foo bar 2 3'.split())
        self.assertEqual(args.foo, 'bar')
        self.assertEqual(args.cmd, 'doit')
        self.assertSequenceEqual(args.rest, [1, 2, 3])
        self.assertIsInstance(args, Arguments)

    def test_parse_intermixed_args_no_ns(self) -> None:
        parser = TypedArgumentParser()
        parser.add_argument('--foo')
        parser.add_argument('cmd')
        parser.add_argument('rest', nargs='*', type=int)
        args = parser.parse_intermixed_args('doit 1 --foo bar 2 3'.split())
        self.assertEqual(args.foo, 'bar')
        self.assertEqual(args.cmd, 'doit')
        self.assertSequenceEqual(args.rest, [1, 2, 3])
        self.assertIsInstance(args, argparse.Namespace)

    def test_parse_intermixed_args_extra_ns(self) -> None:
        class Arguments(argparse.Namespace):
            foo: str
            cmd: str
            rest: list[int]
        parser = TypedArgumentParser()
        parser.add_argument('--foo')
        parser.add_argument('cmd')
        parser.add_argument('rest', nargs='*', type=int)
        args = parser.parse_intermixed_args('doit 1 --foo bar 2 3'.split(), namespace=Arguments())
        self.assertEqual(args.foo, 'bar')
        self.assertEqual(args.cmd, 'doit')
        self.assertSequenceEqual(args.rest, [1, 2, 3])
        self.assertIsInstance(args, Arguments)

    def test_parse_known_intermixed_args(self) -> None:
        class Arguments(TypedNamespace):
            foo: str = argument('--foo')
            cmd: str = argument('cmd')
        args, rest = Arguments.parser().parse_known_intermixed_args('doit 1 --foo bar 2 3'.split())
        self.assertEqual(args.foo, 'bar')
        self.assertEqual(args.cmd, 'doit')
        self.assertSequenceEqual(rest, ['1', '2', '3'])
        self.assertIsInstance(args, Arguments)

    def test_parse_known_intermixed_args_no_ns(self) -> None:
        parser = TypedArgumentParser()
        parser.add_argument('--foo')
        parser.add_argument('cmd')
        args, rest = parser.parse_known_intermixed_args('doit 1 --foo bar 2 3'.split())
        self.assertEqual(args.foo, 'bar')
        self.assertEqual(args.cmd, 'doit')
        self.assertSequenceEqual(rest, ['1', '2', '3'])
        self.assertIsInstance(args, argparse.Namespace)

    def test_parse_known_intermixed_args_extra_ns(self) -> None:
        class Arguments(argparse.Namespace):
            foo: str
            cmd: str
        parser = TypedArgumentParser()
        parser.add_argument('--foo')
        parser.add_argument('cmd')
        args, rest = parser.parse_known_intermixed_args('doit 1 --foo bar 2 3'.split(), namespace=Arguments())
        self.assertEqual(args.foo, 'bar')
        self.assertEqual(args.cmd, 'doit')
        self.assertSequenceEqual(rest, ['1', '2', '3'])
        self.assertIsInstance(args, Arguments)
