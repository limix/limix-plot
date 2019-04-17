def load_dataset(name):
    """
    Example datasets.

    Parameters
    ----------
    name : str
        Possible dataset names are ``"kinship"``, ``"dali"``, and ``"gwas"``.

    Returns
    -------
    data : ndarray, dataframe
        Selected dataset.
    """
    import io
    from bz2 import decompress
    from pandas import read_pickle
    from numpy import load
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
        return read_pickle(io.BytesIO(o), compression=None)

    raise ValueError("Unknown dataset {}.".format(name))
