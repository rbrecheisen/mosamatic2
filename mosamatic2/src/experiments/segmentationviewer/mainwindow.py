import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from widgets.matplotlibcanvas import MatplotlibCanvas


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 + Matplotlib")

        central = QWidget()
        layout = QVBoxLayout(central)

        self.canvas = MatplotlibCanvas(self)
        layout.addWidget(self.canvas)

        btn = QPushButton("Plot")
        btn.clicked.connect(self.plot_example)
        layout.addWidget(btn)

        self.setCentralWidget(central)

    def plot_example(self):
        ax = self.canvas.axes()
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
