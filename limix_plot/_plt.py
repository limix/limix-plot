def get_pyplot():
    from sys import platform as sys_pf

    if get_pyplot.pyplot is not None:
        return get_pyplot.pyplot

    if sys_pf == "darwin":
        from matplotlib import use as _backend_use

        _backend_use("TkAgg")

    from matplotlib import pyplot

    return pyplot


get_pyplot.pyplot = None
