from os import environ as _environ


def get_pyplot():
    if get_pyplot.pyplot is not None:
        return get_pyplot.pyplot

    if "DISPLAY" not in _environ:
        from matplotlib import use as _backend_use

        _backend_use("Agg")
    from matplotlib import pyplot

    return pyplot


get_pyplot.pyplot = None
