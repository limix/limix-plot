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
from .normal import normal
from .power import power
from .consensus import ConsensusCurve

__version__ = '0.0.2'

__all__ = ['__version__', 'qqplot', 'box_aspect', 'load_dataset', 'test',
           'kinship', 'image', 'manhattan', 'pca', 'normal', 'power',
           'ConsensusCurve']
