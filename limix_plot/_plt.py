def get_pyplot():
    from sys import platform as sys_pf
    from matplotlib import rcParams

    if get_pyplot.pyplot is not None:
        return get_pyplot.pyplot

    if "backend" not in rcParams and sys_pf == "darwin":
        from matplotlib import use as _backend_use

        _backend_use("TkAgg")

    from matplotlib import pyplot

    get_pyplot.pyplot = pyplot

    return pyplot


get_pyplot.pyplot = None
