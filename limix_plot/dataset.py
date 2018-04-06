import sys
import io
import numpy as np

PY2 = sys.version_info < (3, )

if PY2:
    from urllib import urlopen
else:
    from urllib.request import urlopen


def load_dataset(name):
    if name == 'kinship':
        c = urlopen("http://rest.s3for.me/limix/1000G_kinship.npy").read()
        f = io.BytesIO(c)
        return np.load(f)
    raise ValueError("Unknown dataset {}.".format(name))
