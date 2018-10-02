from ._plt import get_pyplot


def image(file, ax=None):
    r"""Show an image.

    Parameters
    ----------
    file : file-like object, string, or pathlib.Path
        The file to read.
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
        >>>
        >>> plt = get_pyplot()
        >>> file = lp.load_dataset("dali")
        >>> lp.image(file)  # doctest: +SKIP
        >>> file.close()
    """
    import imghdr
    from numpy.compat import basestring, is_pathlib_path

    plt = get_pyplot()

    ax = plt.gca() if ax is None else ax

    own_fid = False
    if isinstance(file, basestring):
        fid = open(file, "rb")
        own_fid = True
    elif is_pathlib_path(file):
        fid = file.open("rb")
        own_fid = True
    else:
        fid = file

    try:
        ax.imshow(plt.imread(fid, format=imghdr.what(fid)))
        ax.set_position([0, 0, 1, 1])
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
    finally:
        if own_fid:
            fid.close()

    return ax
