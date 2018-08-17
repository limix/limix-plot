r"""Plotting library for genetics."""

from __future__ import absolute_import

from os import environ as _environ

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
from .testit import test


def get_pyplot():
    if get_pyplot.pyplot is not None:
        return get_pyplot.pyplot

    if "DISPLAY" not in _environ:
        from matplotlib import use as _backend_use

        _backend_use("Agg")
    from matplotlib import pyplot

    return pyplot


get_pyplot.pyplot = None

__version__ = "0.0.3"

__all__ = [
    "ConsensusCurve",
    "__version__",
    "box_aspect",
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
