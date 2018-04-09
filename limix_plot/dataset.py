import sys
import io
import bz2
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
    elif name == 'dali':
        c = urlopen("http://rest.s3for.me/limix/dali.jpg.bz2").read()
        o = bz2.decompress(c)
        return io.BytesIO(o)
    elif name == 'gwas':
        c = urlopen("http://rest.s3for.me/limix/mdd4.pkl.bz2").read()
        o = bz2.decompress(c)
        return io.BytesIO(o)

    raise ValueError("Unknown dataset {}.".format(name))


# import sys
# import bz2
# import io
# import limix_plot as lp
# from matplotlib import pyplot as plt
#
# PY2 = sys.version_info < (3, )
#
# if PY2:
#     from urllib import urlopen
# else:
#     from urllib.request import urlopen
#
# lp.image(f)
# plt.show()
