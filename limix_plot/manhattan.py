from __future__ import division

import pandas as pd
from matplotlib import pyplot as plt
from numpy import asarray, cumsum, flipud, log10, unique


def manhattan(data, pv='pv', pos='pos', chr='chr', colora='#5689AC',
              colorb='#21334F', pts_kws=None, ax=None):
    r"""Produce a manhattan plot.

    Parameters
    ----------
    data : DataFrame, dict
        DataFrame containing the chromosome, base-pair positions, and
        p-values.
    pv : str
        Column name for the p-values. Defaults to ``"pv"``.
    pos : str
        Column name for the base-pair positions. Defaults to ``"pos"``.
    chr : str
        Column name for the chromosomes. Defaults to ``"chr"``.
    colora : matplotlib color
        Points color of the first group.
    colorb : matplotlib color
        Points color of the second group.
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
        :include-source:

        >>> from matplotlib import pyplot as plt
        >>> import limix_plot as lp
        >>> from numpy import log10
        >>>
        >>> df = lp.load_dataset('gwas')
        >>> print(df.head())
        >>> lp.manhattan(df)
        >>> ax = plt.gca()
        >>> plt.axhline(-log10(1e-7), color='red')
        >>> ax.set_ylim(2, ax.get_ylim()[1])
        >>> plt.show()
    """
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data=data)

    if pts_kws is None:
        pts_kws = dict()

    df = data.loc[:, [pv, pos, chr]].copy()
    df = df.rename(columns={pv: 'pv', pos: 'pos', chr: 'chr'})

    ax = plt.gca() if ax is None else ax

    df['chr'] = df['chr'].astype(str)
    df['pos'] = df['pos'].astype(int)
    df['pv'] = df['pv'].astype(float)
    chr_order = _chr_precedence(df)
    df = df.assign(order=[chr_order[i] for i in df['chr'].values])
    df = df.sort_values(by=['order', 'pos'])

    df = _abs_pos(df)

    if 'markersize' not in pts_kws:
        pts_kws['markersize'] = 2
    if 'marker' not in pts_kws:
        pts_kws['marker'] = '.'
    if 'linestyle' not in pts_kws:
        pts_kws['linestyle'] = ''

    colors = {0: colora, 1: colorb}

    for i, c in enumerate(unique(df['order'])):
        ok = df['order'] == c
        pts_kws['color'] = colors[i % 2]
        x = df.loc[ok, 'abs_pos']
        y = -log10(df.loc[ok, 'pv'])
        ax.plot(x, y, **pts_kws)

    ax.set_xlim(df['abs_pos'].min(), df['abs_pos'].max())
    ax.set_ylim(0, ax.get_ylim()[1])

    ax.set_ylabel('-log$_{10}$pv')
    ax.set_xlabel('chromosome')

    u = unique(df['chr'].values)
    chrom_labels = sorted(u, key=lambda x: chr_order[x])
    _set_ticks(ax, _chrom_bounds(df), chrom_labels)

    return ax


def _plot_points(ax, df, alpha, null_style, alt_style):

    null_df = df.loc[df['pv'] >= alpha, :]
    alt_df = df.loc[df['pv'] < alpha, :]

    ax.plot(null_df['abs_pos'], -log10(null_df['pv']), '.', ms=7, **null_style)
    ax.plot(alt_df['abs_pos'], -log10(alt_df['pv']), '.', ms=7, **alt_style)


def _plot_chrom_strips(ax, df, ytop):
    order = df['order'].unique()
    for i in range(0, len(order), 2):
        ax.fill_between(
            df['abs_pos'],
            0,
            ytop,
            where=df['order'] == order[i],
            facecolor='black',
            edgecolor='black',
            linewidth=0,
            alpha=0.1)


def _set_ticks(ax, chrom_bounds, chrom_labels):
    n = len(chrom_bounds) - 1
    xticks = asarray([chrom_bounds[i:i + 2].mean() for i in range(n)])
    ax.set_xticks(xticks)
    ax.set_xticklabels(chrom_labels)


def _abs_pos(df):
    order = df['order'].unique()
    chrom_ends = [df['pos'][df['order'] == c].max() for c in order]

    offset = flipud(cumsum(chrom_ends)[:-1])

    df['abs_pos'] = df['pos'].copy()

    order = list(reversed(order))
    for i, oi in enumerate(offset):
        ix = df['order'] == order[i]
        df.loc[ix, 'abs_pos'] = df.loc[ix, 'abs_pos'] + oi

    return df


def _chrom_bounds(df):
    order = df['order'].unique()
    v = [df['abs_pos'][df['order'] == c].min() for c in order]
    return asarray(v + [df['abs_pos'].max()])


def _isint(i):
    try:
        int(i)
    except ValueError:
        return False
    else:
        return True


def _chr_precedence(df):
    uchr = unique(df['chr'].values)
    nchr = [int(i) for i in uchr if _isint(i)]
    precedence = {str(i): i for i in nchr}
    schr = sorted([i for i in uchr if not _isint(i)])
    for i, s in enumerate(schr):
        precedence[s] = max(nchr) + i + 1
    return precedence
