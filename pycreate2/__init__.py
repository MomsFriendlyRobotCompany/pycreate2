##############################################
# The MIT License (MIT)
# Copyright (c) 2017 Kevin Walchko
# see LICENSE for full details
##############################################

try:
    from importlib.metadata import version # type: ignore
except ImportError:
    from importlib_metadata import version # type: ignore

from .create2api import Create2

__license__ = 'MIT'
__author__ = 'Kevin Walchko'
__version__ = version("pycreate2")
