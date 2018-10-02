from __future__ import division

from ._plt import get_pyplot


def power(pv, label=None, alphas=None, pts_kws=None, ax=None):
    r"""Plot number of hits across significance levels.

    Parameters
    ----------
    pv : array_like
        P-values.
    label : string, optional
        Legend label for the relevent component of the plot.
    alphas : array_like, optional
        Significance thresholds for which the number of hits is defined.
        Defaults to ``numpy.linspace(0.01, 0.5, 500)``.
    pts_kws : dict, optional
        Keyword arguments forwarded to the matplotlib function used for
        plotting the points.
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

        >>> from limix_plot import get_pyplot
        >>> import limix_plot as lp
        >>> from numpy.random import RandomState
        >>>
        >>> plt = get_pyplot()
        >>> random = RandomState(1)
        >>> nsnps = 10000
        >>>
        >>> pv0 = list(random.rand(nsnps))
        >>> pv1 = list(0.7 * random.rand(nsnps))
        >>>
        >>> lp.power(pv0, label='label0')  # doctest: +SKIP
        >>> ax = lp.power(pv1, label='label1')
        >>> ax.legend(loc='best')  # doctest: +SKIP
    """
    from numpy import asarray, linspace

    plt = get_pyplot()

    pv = asarray(pv).ravel()

    if alphas is None:
        alphas = linspace(0.01, 0.5, 500)

    ax = plt.gca() if ax is None else ax

    if pts_kws is None:
        pts_kws = dict()
    if "label" not in pts_kws:
        pts_kws["label"] = label

    nhits = _collect_nhits(pv, alphas)
    ax.plot(alphas, asarray(nhits, int), **pts_kws)

    ax.set_xlabel("significance level")
    ax.set_ylabel("number of hits")

    return ax


def _collect_nhits(pv, alphas):
    from numpy import asarray

    nhits = []

    for alpha in alphas:
        n = (pv < alpha).sum()
        nhits += [n]

    return asarray(nhits, int)
