def show():
    import matplotlib as mpl

    if mpl.get_backend().lower() == "agg":
        return None

    from limix import plot

    plt = plot.get_pyplot()
    return plt.show()
