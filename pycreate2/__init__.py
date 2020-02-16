# The MIT License
#
# Copyright (c) 2017 Kevin Walchko

try:
    from importlib_metadata import version # type: ignore
except ImportError:
    from importlib.metadata import version # type: ignore

from .create2api import Create2
# from .create2api import Fatal, Error, Warning

# from .version import __version__

__license__ = 'MIT'
__author__ = 'Kevin Walchko'
# __version__ = '0.7.4'
__version__ = version("pycreate2")
