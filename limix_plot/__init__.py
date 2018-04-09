r"""Plotting library for genetics."""

from __future__ import absolute_import as _
from .kinship import kinship
from .qqplot import qqplot
from .misc import box_aspect
from .testit import test
from .dataset import load_dataset
from .image import image
from .manhattan import manhattan
from .pca import pca

__version__ = '0.0.1'

__all__ = ['__version__', 'qqplot', 'box_aspect', 'load_dataset', 'test',
           'kinship', 'image', 'manhattan', 'pca']
