"""
Plotting library for genetics.
"""

from ._consensus import ConsensusCurve
from ._dataset import load_dataset
from ._image import image
from ._kinship import kinship
from ._manhattan import manhattan
from ._misc import box_aspect
from ._normal import normal
from ._pca import pca
from ._plt import get_pyplot
from ._power import power
from ._qqplot import qqplot
from ._show import show
from ._testit import test

__version__ = "0.1.0"

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
    "show",
]
