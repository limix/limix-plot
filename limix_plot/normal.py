import matplotlib.pyplot as plt
import scipy.stats as st
from numpy import arange, asarray
from numpy import mean as _mean
from numpy import std as _std


def normal(x, bins=20, nstd=2, ax=None):
    r"""Plot a fit of a normal distribution to the data in x.

    Parameters
    ----------
    x : array_like
        Values to be fitted.
    bins : int, optional
        Number of histogram bins. Defaults to ``20``.
    nstd : float, optional
        Standard deviation multiplier for drawing a dashed line.
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

        >>> from numpy.random import RandomState
        >>> from matplotlib import pyplot as plt
        >>> import limix_plot as lp
        >>>
        >>> random = RandomState(10)
        >>> x = random.randn(100)
        >>> lp.normal(x)
        >>> plt.show()
    """

    x = asarray(x).ravel()

    ax = plt.gca() if ax is None else ax

    mean_x = _mean(x)
    std_x = _std(x)

    xvals = arange(mean_x - 5 * std_x, mean_x + 5 * std_x, .001)
    yvals = st.norm.pdf(xvals, mean_x, std_x)

    ax.hist(x, bins, density=True)

    ax.plot(xvals, yvals, color='red')

    _draw_normal(ax, mean_x, std_x, nstd, 'red')

    return ax


def _draw_normal(axis, mean, scale, nstd, color):
    max_pdf = st.norm.pdf(mean, mean, scale)

    axis.plot([mean, mean], [0, max_pdf], color=color, linestyle="--")

    axis.annotate(
        '$\mu$',
        xy=(mean + 0.6 * scale, max_pdf),
        horizontalalignment='center',
        verticalalignment='bottom',
        color=color)

    top = st.norm.pdf(mean + nstd * scale, mean, scale)
    left = mean - nstd * scale
    right = mean + nstd * scale

    axis.plot([right, right], [0, top], color=color, linestyle="--")

    axis.plot([left, left], [0, top], color=color, linestyle="--")

    if int(nstd) == nstd:
        mu_sigma = '$\mu+%d\sigma$' % nstd
    else:
        mu_sigma = '$\mu+%.1f\sigma$' % nstd

    axis.annotate(
        mu_sigma,
        xy=(mean + (1.2 + nstd) * scale, top),
        horizontalalignment='center',
        verticalalignment='bottom',
        color=color)
