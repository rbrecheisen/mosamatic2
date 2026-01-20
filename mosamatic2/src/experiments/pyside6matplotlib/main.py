# pip install matplotlib PySide6
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 + Matplotlib")

        central = QWidget()
        layout = QVBoxLayout(central)

        self.canvas = MplCanvas(self, width=6, height=4, dpi=100)
        layout.addWidget(self.canvas)

        btn = QPushButton("Plot")
        btn.clicked.connect(self.plot_example)
        layout.addWidget(btn)

        self.setCentralWidget(central)
        # self.plot_example()

    def plot_example(self):
        ax = self.canvas.ax
        ax.clear()
        x = [0, 1, 2, 3, 4]
        y = [0, 1, 4, 9, 16]
        ax.plot(x, y)
        ax.set_title("Embedded Matplotlib")
        ax.figure.tight_layout()
        self.canvas.draw()          # draw() for immediate update
        # self.canvas.draw_idle()   # nicer if you update often


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.resize(800, 600)
    w.show()
    sys.exit(app.exec())
