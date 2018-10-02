r"""Plotting library for genetics."""

from __future__ import absolute_import

from ._plt import get_pyplot
from ._testit import test
from .consensus import ConsensusCurve
from .dataset import load_dataset
from .image import image
from .kinship import kinship
from .manhattan import manhattan
from .misc import box_aspect
from .normal import normal
from .pca import pca
from .power import power
from .qqplot import qqplot

__version__ = "0.0.6"

__all__ = [
    "__version__",
    "box_aspect",
    "ConsensusCurve",
    "get_pyplot",
    "image",
    "kinship",
    "load_dataset",
    "manhattan",
    "normal",
    "pca",
    "power",
    "qqplot",
    "test",
]
