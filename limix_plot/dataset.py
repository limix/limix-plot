import sys
import io
import bz2
import numpy as np
from pandas import read_pickle

PY2 = sys.version_info < (3, )

if PY2:
    from urllib import urlopen
else:
    from urllib.request import urlopen


def load_dataset(name):
    r"""Example datasets.

    Parameters
    ----------
    name : str
        Possible dataset names are ``"kinship"``, ``"dali"``, and ``"gwas"``.

    Returns
    -------
    Numpy array, BytesIO, DataFrame : Selected dataset.
    """
    if name == 'kinship':
        c = urlopen("http://rest.s3for.me/limix/1000G_kinship.npy").read()
        f = io.BytesIO(c)
        return np.load(f)
    elif name == 'dali':
        c = urlopen("http://rest.s3for.me/limix/dali.jpg.bz2").read()
        o = bz2.decompress(c)
        return io.BytesIO(o)
    elif name == 'gwas':
        c = urlopen("http://rest.s3for.me/limix/mdd_small.pkl.bz2").read()
        o = bz2.decompress(c)
        return read_pickle(io.BytesIO(o))

    raise ValueError("Unknown dataset {}.".format(name))
