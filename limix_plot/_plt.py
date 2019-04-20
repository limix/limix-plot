def get_pyplot():
    """
    Get :mod:`matplotlib.pyplot`.

    Returns
    -------
    pyplot : :mod:`matplotlib.pyplot`
        MATLAB-like interface.
    """
    from sys import platform as sys_pf
    from matplotlib import rcParams

    if get_pyplot.pyplot is not None:
        return get_pyplot.pyplot

    # Bug with matplotlib on macos:
    # https://github.com/matplotlib/matplotlib/issues/10239
    if "backend" not in rcParams and sys_pf == "darwin":
        from matplotlib import use as _backend_use

        _backend_use("TkAgg")

    from matplotlib import pyplot

    get_pyplot.pyplot = pyplot


get_pyplot.pyplot = None
