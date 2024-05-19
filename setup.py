#!/usr/bin/python
""" Setup file for crccheck package.

  License::

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

"""
from setuptools import setup
import pathlib


setup(
    name='ArgParseTyped',
    description='argparse parameter namespaces with type hints',
    long_description_content_type='text/x-rst',
    long_description=pathlib.Path("README.rst").read_text(),
    author='Martin Scharrer',
    author_email='martin.scharrer@web.de',
    license='MIT',
    license_files=['LICENSE.txt'],
    packages=['argparse_typed'],
    test_suite='tests',
    version='0.1.0',
    url='https://github.com/MartinScharrer/argparse_typed',
    install_requires=[],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development",
        "Typing :: Typed",
    ],
)