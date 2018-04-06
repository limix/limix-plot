r"""Plotting library for genetics."""

from __future__ import absolute_import as _
from .qqplot import qqplot
from .misc import box_aspect
from .testit import test

__version__ = '0.0.1'

__all__ = ['__version__', 'qqplot', 'box_aspect', 'test']
