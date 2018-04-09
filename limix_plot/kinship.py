from __future__ import division

import warnings
from numpy import argsort, asarray, clip, inf, percentile
import matplotlib.pyplot as plt


def kinship(K, nclusters=1, img_kws=None, ax=None):
    r"""Plot heatmap of a kinship matrix.

    Parameters
    ----------
    K : 2d-array
        Kinship matrix.
    nclusters : int, str, optional
        Number of blocks to be seen from the heatmap. It defaults to ``1``,
        which means that no ordering is performed. Pass ``"auto"`` to
        automatically determine the number of clusters. Pass an integer to
        select the number of clusters.
    img_kws : dict, optional
        Keyword arguments forwarded to the matplotlib pcolormesh function.
    ax : matplotlib Axes, optional
        The target handle for this figure. If ``None``, the current axes is
        set.

    Returns
    -------
    ax : matplotlib Axes
        Axes object with the plot for further tweaking.

    Examples
    --------
    .. plot::
        :include-source:

        >>> import limix_plot as lp
        >>> from matplotlib import pyplot as plt
        >>>
        >>> K = lp.load_dataset("kinship")
        >>> lp.kinship(K)
        >>> plt.show()
    """

    ax = plt.gca() if ax is None else ax

    if img_kws is None:
        img_kws = dict()
    if 'cmap' not in img_kws:
        img_kws['cmap'] = 'RdBu_r'

    K = asarray(K, float)
    if nclusters == 'auto':
        K = _infer_clustering(K)
    elif nclusters > 1:
        K = _clustering(K, nclusters)

    cmin = percentile(K, 2)
    cmax = percentile(K, 98)
    K = clip(K, cmin, cmax)
    K = (K - K.min()) / (K.max() - K.min())

    mesh = ax.pcolormesh(K, **img_kws)

    ax.set_aspect("equal")
    ax.set(xlim=(0, K.shape[1]), ylim=(0, K.shape[0]))
    ax.xaxis.set_ticks([])
    ax.yaxis.set_ticks([])
    ax.figure.colorbar(mesh, None, ax)

    return ax


def _infer_clustering(K):
    from sklearn.metrics import silhouette_score

    scores = []
    nclusterss = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    for nclusters in nclusterss:
        labels = _cluster(K, nclusters)
        # idx = argsort(labels)

        s = silhouette_score(K, labels, metric='correlation')
        scores.append(s)

    smallest = inf
    nclusters = -1
    for i in range(1, len(nclusterss)):
        d = scores[i] - scores[i - 1]
        if d < smallest:
            smallest = d
            nclusters = nclusterss[i - 1]

    return _clustering(K, nclusters)


def _cluster(K, n):
    from sklearn.cluster import SpectralClustering

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        m = SpectralClustering(n_clusters=n)
        m.fit(K)

    return m.labels_


def _clustering(K, n):
    idx = argsort(_cluster(K, n))
    return K[idx, :][:, idx]
