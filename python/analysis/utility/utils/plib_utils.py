import sys
import os

def import_matplotlib() :
    on_brick = os.environ.get("ON_BRICK", "0")
    import matplotlib
    if on_brick == "0" :
        matplotlib.use("pdf")
    return matplotlib
def import_pyplot() :
    on_brick = os.environ.get("ON_BRICK", "0")
    if on_brick == "0" :
        import matplotlib.pyplot as plt
        return plt
    elif on_brick == "1" :
        import matplotlib
        matplotlib.use("pdf")
        import matplotlib.pyplot as plt
        return plt
