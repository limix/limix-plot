import io
import sys

PY2 = sys.version_info < (3,)


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

    from bz2 import decompress
    from pandas import read_pickle
    from numpy import load

    if PY2:
        from urllib import urlopen
    else:
        from urllib.request import urlopen

    if name == "kinship":
        c = urlopen("http://rest.s3for.me/limix/1000G_kinship.npy").read()
        f = io.BytesIO(c)
        return load(f)
    elif name == "dali":
        c = urlopen("http://rest.s3for.me/limix/dali.jpg.bz2").read()
        o = decompress(c)
        return io.BytesIO(o)
    elif name == "gwas":
        c = urlopen("http://rest.s3for.me/limix/mdd_small.pkl.bz2").read()
        o = decompress(c)
        return read_pickle(io.BytesIO(o))

    raise ValueError("Unknown dataset {}.".format(name))
