from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MatplotlibCanvas(FigureCanvas):
    def __init__(self, parent, nrows=1, ncols=1, width=6, height=4, dpi=100):
        self._figure = Figure(figsize=(width, height), dpi=dpi)
        self._axes = self._figure.subplots(nrows, ncols)
        super(MatplotlibCanvas, self).__init__(self._figure)
        self.setParent(parent)
        self._nrows = nrows
        self._ncols = ncols
        self._navtoolbar = None

    def axes(self, idx=0, idy=0):
        assert idx<self._nrows and idy<self._ncols
        if idx>0 and idy>0:
            return self._axes[idx, idy]
        elif idx>0:
            return self._axes[idx]
        else:
            return self._axes
        
    def navtoolbar(self):
        if not self._navtoolbar:
            self._navtoolbar = NavigationToolbar(self, self.parent())
        return self._navtoolbar