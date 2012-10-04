"""
============
Introduction
============
The plumbing software is a package written in Python. It is designed to help with plumbing-type programmation.

============
Installation
============
To install you can simply type::

    $ sudo easy_install plumbing

That's it. However, if that doesn't work because you don't have sufficient permissions, you can simply install it somewhere else (for instance in your home)::

    $ easy_install --user plumbing
"""

b'This module needs Python 2.6 or later.'

# Special variables #
__version__ = '1.1.1'

# Export some objects #
from cmd import command