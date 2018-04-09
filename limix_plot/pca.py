from __future__ import division

from numpy import asarray
import matplotlib.pyplot as plt
from sklearn import decomposition


def pca(X, pts_kws=None, ax=None):
    r"""Plot the first two principal components of a design matrix.

    Parameters
    ----------
    X : array_like
        Design matrix: samples by features.
    pts_kws : dict, optional
        Keyword arguments forwarded to the matplotlib pcolormesh function.
    ax : matplotlib Axes, optional
        The target handle for this figure. If ``None``, the current axes is
        set.

    Returns
    -------
    ax : matplotlib Axes
        Axes object with the plot for further tweaking.

    Example
    -------
    .. plot::
        :include-source:

        >>> import limix_plot as lp
        >>> from matplotlib import pyplot as plt
        >>> from numpy.random import RandomState
        >>>
        >>> random = RandomState(0)
        >>> X = random.randn(30, 10)
        >>> lp.pca(X)
        >>> plt.show()
    """

    ax = plt.gca() if ax is None else ax

    if pts_kws is None:
        pts_kws = dict()

    if 'marker' not in pts_kws:
        pts_kws['marker'] = 'o'
    if 'linestyle' not in pts_kws:
        pts_kws['linestyle'] = ''
    if 'markersize' not in pts_kws:
        pts_kws['markersize'] = 4

    X = asarray(X, float)

    pca = decomposition.PCA(n_components=2)
    pca.fit(X)
    X = pca.transform(X)

    ax.plot(X[:, 0], X[:, 1], **pts_kws)

    ax.set_xlabel('first component')
    ax.set_ylabel('second component')

    return ax
