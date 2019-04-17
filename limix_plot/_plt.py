def get_pyplot():
    """
    Get :mod:`matplotlib.pyplot`.

    Returns
    -------
    pyplot : :mod:`matplotlib.pyplot`
        MATLAB-like interface.
    """
    from matplotlib import pyplot

    if get_pyplot.pyplot is None:
        get_pyplot.pyplot = pyplot

    return get_pyplot.pyplot


get_pyplot.pyplot = None
