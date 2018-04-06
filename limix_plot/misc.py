from numpy import inf
from matplotlib import pyplot as plt


def box_aspect(ax=None):
    r"""Change to box aspect considering the plotted points.

    ax : matplotlib axis, optional
        If provided, work on this axis.

    Returns
    -------
    ax : matplotlib Axes
        Returns the Axes object with the plot for further tweaking.
    """
    if ax is None:
        ax = plt.gca()

    xlim = [+inf, -inf]
    ylim = [+inf, -inf]
    for line in ax.get_lines():
        xlim[0] = min(xlim[0], min(line.get_xdata()))
        xlim[1] = max(xlim[1], max(line.get_xdata()))

        ylim[0] = min(ylim[0], min(line.get_ydata()))
        ylim[1] = max(ylim[1], max(line.get_ydata()))

    mi = min(xlim[0], ylim[0])
    ma = max(xlim[1], ylim[1])

    ax.set_xlim(mi, ma)
    ax.set_ylim(mi, ma)

    ax.set_aspect('equal', 'box')
    ax.apply_aspect()

    ticks = ax.get_yticks()
    ymax = ax.get_xbound()[1]
    ticks = [t for t in ticks if t < ymax]

    ax.set_xticks(ticks)
    ax.set_yticks(ticks)

    return ax
