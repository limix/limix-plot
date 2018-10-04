def pytest_sessionstart(*args, **kwargs):
    import matplotlib as mpl

    mpl.use("agg")
