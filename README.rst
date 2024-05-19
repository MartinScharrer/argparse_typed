argparse_typed - Type hints for argparse parameter namespaces
=============================================================


Usage example::

    from argparse_typed import TypedNamespace

    class Arguments(TypedNamespace):
        input: str = argument('-i', '--input')
        output: str = argument('-o', '--output')
        hex: bool = argument('-H', '--hex', action='store_true')
        val: float = argument('-V', default=0.0)

    parser = Arguments.parser()
    args: Arguments = parser.parse_args([...])

    # args.input will be identified as 'str'

License:
    MIT License

    Copyright (c) 2024 by Martin Scharrer <martin.scharrer@web.de>

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software
    and associated documentation files (the "Software"), to deal in the Software without
    restriction, including without limitation the rights to use, copy, modify, merge, publish,
    distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or
    substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
    BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
    DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
