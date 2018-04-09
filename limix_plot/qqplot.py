from __future__ import division

from numpy import (arange, ascontiguousarray, flipud, linspace, log10, ones,
                   percentile, searchsorted, sort, asarray)
from numpy import sum as npsum
from numpy import where
from scipy.special import betaincinv
import matplotlib.pyplot as plt


def qqplot(a, label=None, alpha=0.05, cutoff=0.1, line=True, pts_kws=None,
           band_kws=None, ax=None):
    r"""Quantile-Quantile plot of observed p-values versus theoretical ones.

    Parameters
    ----------
    a : Series, 1d-array, list
        Observed p-values.
    label : string, optional
        Legend label for the relevent component of the plot.
    alpha : float, optional
        Significance level defining the confidfence interval. Set to ``None``
        to disable plotting. Defaults to ``0.05``.
    cutoff : float, optional
        P-values higher than `cutoff` will not be plotted. Defaults to ``0.1``.
    line : bool, optional
        Whether or not plot a straight line. Defaults to ``True``.
    pts_kws : dict, optional
        Keyword arguments forwarded to the matplotlib function used for
        plotting the points.
    band_kws : dict, optional
        Keyword arguments forwarded to the fill_between function used for
        plotting the confidence band.
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

        >>> import matplotlib.pyplot as plt
        >>> import limix_plot as lp
        >>> from numpy.random import RandomState
        >>>
        >>> random = RandomState(1)
        >>>
        >>> pv0 = random.rand(10000)
        >>> pv0[0] = 1e-6
        >>>
        >>> pv1 = random.rand(10000)
        >>> pv2 = random.rand(10000)
        >>>
        >>> lp.qqplot(pv0)
        >>> plt.show()

        >>> lp.qqplot(pv0)
        >>> lp.qqplot(pv1, line=False, alpha=None)
        >>> plt.show()

        >>> lp.qqplot(pv1)
        >>> lp.qqplot(pv2, line=False, alpha=None)
        >>> lp.box_aspect()
        >>> plt.show()

        >>> lp.qqplot(pv0, label='label0', band_kws=dict(color='#EE0000',
        ...                                              alpha=0.2))
        >>> lp.qqplot(pv1, label='label1', line=False, alpha=None)
        >>> ax = lp.qqplot(pv2, label='label2', line=False,
        ...                alpha=None, pts_kws=dict(marker='*'))
        >>> ax.legend()
        >>> plt.show()
    """

    a = asarray(a)
    if a.ndim > 1:
        a = a.squeeze()

    if ax is None:
        ax = plt.gca()

    if pts_kws is None:
        pts_kws = dict()
    if 'marker' not in pts_kws:
        pts_kws['marker'] = 'o'
    if 'linestyle' not in pts_kws:
        pts_kws['linestyle'] = ''
    if 'markeredgecolor' not in pts_kws:
        pts_kws['markeredgecolor'] = None
    if label is not None:
        pts_kws['label'] = label

    if band_kws is None:
        band_kws = dict()
    if 'facecolor' not in band_kws:
        band_kws['facecolor'] = '#DDDDDD'
    if 'linewidth' not in band_kws:
        band_kws['linewidth'] = 0
    if 'zorder' not in band_kws:
        band_kws['zorder'] = -1
    if 'alpha' not in band_kws:
        band_kws['alpha'] = 1.0

    pv = sort(a)
    ok = _subsample(pv, cutoff)

    qnull = -log10((0.5 + arange(len(pv))) / len(pv))
    qemp = -log10(pv)

    ax.plot(qnull[ok], qemp[ok], **pts_kws)

    qmax = max(qnull[ok].max(), qemp[ok].max())

    xmin = qnull[ok].min()
    xmax = qnull[ok].max()

    if line:
        ax.plot([xmin, xmax], [xmin, xmax], color='black', zorder=0)

    if alpha is not None:
        _plot_confidence_band(ok, qnull, alpha, ax, qmax, band_kws)

    ax.set_ylabel('-log$_{10}$pv observed')
    ax.set_xlabel('-log$_{10}$pv expected')

    ax.xaxis.set_ticks_position('both')
    ax.yaxis.set_ticks_position('both')

    return ax


def _expected(n):
    lnpv = linspace(1 / (n + 1), n / (n + 1), n, endpoint=True)
    return flipud(-log10(lnpv))


def _rank_confidence_band(nranks, significance_level, ok):
    alpha = significance_level

    k0 = arange(1, nranks + 1)
    k1 = flipud(k0).copy()

    k0 = ascontiguousarray(k0[ok])
    k1 = ascontiguousarray(k1[ok])

    top = betaincinv(k0, k1, 1 - alpha)
    bottom = betaincinv(k0, k1, alpha)

    return (bottom, top)


def _plot_confidence_band(ok, null_qvals, significance_level, ax, qmax,
                          band_kws):

    (bo, to) = _rank_confidence_band(len(null_qvals), significance_level, ok)

    bo = -log10(bo)
    to = -log10(to)

    m = null_qvals[ok]

    ax.fill_between(m, bo, to, **band_kws)


def _subsample(pvalues, cutoff):
    resolution = 500

    if len(pvalues) <= resolution:
        return ones(len(pvalues), dtype=bool)

    ok = pvalues <= percentile(pvalues, cutoff)
    nok = ~ok

    qv = -log10(pvalues[nok])
    qv_min = qv[-1]
    qv_max = qv[0]

    snok = npsum(nok)

    resolution = min(snok, resolution)

    qv_chosen = linspace(qv_min, qv_max, resolution)
    pv_chosen = 10**(-qv_chosen)

    idx = searchsorted(pvalues[nok], pv_chosen)
    n = sum(nok)
    i = 0
    while i < len(idx) and idx[i] == n:
        i += 1
        idx = idx[i:]

    ok[where(nok)[0][idx]] = True

    ok[0] = True
    ok[-1] = True

    return ok
