from __future__ import absolute_import, division

from numpy import asarray, logical_and, ones, sqrt


class ConsensusCurve(object):
    r"""Consolidate multiple curves in a single one.

    Examples
    --------
    .. plot::
        :include-source:

        >>> from matplotlib import pyplot as plt
        >>> import limix_plot as lp
        >>> from numpy import sort
        >>> from numpy.random import RandomState
        >>>
        >>> random = RandomState(1)
        >>>
        >>> n0 = 30
        >>> x0 = sort(random.rand(n0))
        >>> y0 = 10 * x0 + random.rand(n0)
        >>>
        >>> n1 = 20
        >>> x1 = sort(random.rand(n1))
        >>> y1 = 10 * x1 + random.rand(n1)
        >>>
        >>> cc = lp.ConsensusCurve()
        >>> cc.add(x0, y0)
        >>> cc.add(x1, y1)
        >>>
        >>> (x, ybottom, y, ytop) = cc.consensus()
        >>> plt.plot(x, y)
        >>> ax = plt.gca()
        >>> ax.fill_between(x, ybottom, ytop, lw=0, edgecolor='None',
        ...                 facecolor='blue', alpha=0.25, interpolate=True)
        >>>
        >>> plt.show()
    """

    def __init__(self):
        self._x = []
        self._y = []

    def add(self, x, y):
        r"""Add a new curve.

        Parameters
        ----------
        x : array_like
            x-coordinate values.
        y : array_like
            y-coordinate values.
        """
        self._x.append(asarray(x))
        self._y.append(asarray(y))

    def consensus(self, std_dev=3.0):
        r"""Return a consensus curve.

        Parameters
        ----------
        std_dev : float
            Confidence band width. Defaults to ``3``.

        Returns
        -------
        x : array_like
            x-coordinate values.
        ybottom : array_like
            y-coordinate values of the lower part of the confidence band.
        y : array_like
            y-coordinate values of the mean of the confidence band.
        ytop : array_like
            y-coordinate values of the upper part of the confidence band.
        """
        x = self._x
        y = self._y
        x, ybottom, y, ytop = _consensus_curve(x, y, std_dev=std_dev)

        return (x, ybottom, y, ytop)


def _2dbulk(x, left, right, y):
    xbulk = []
    ybulk = []
    for (i, xi) in enumerate(x):
        ok = logical_and(left <= xi, xi <= right)
        xbulk.append(xi[ok].mean())
        ybulk.append(y[i][ok].mean())

    return (asarray(xbulk), asarray(ybulk))


def _consensus_curve(x, y, std_dev=3.0):
    n = -1
    for xi in x:
        n = max(len(xi), n)

    nx = ones((len(x), n))
    ny = ones((len(y), n))

    for i, xi in enumerate(x):
        nx[i, :len(xi)] = xi

    for i, yi in enumerate(y):
        ny[i, :len(yi)] = yi

    x = nx
    y = ny

    xavg = x.mean(0)
    yavg = y.mean(0)

    err = y.std(0) * std_dev / sqrt(x.shape[0])

    return (xavg, yavg - err, yavg, yavg + err)
