import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import pyqtgraph as pg
import numpy as np


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 + PyQtGraph Example")
        self.resize(600, 400)

        # Central widget
        central = QWidget()
        layout = QVBoxLayout(central)
        self.setCentralWidget(central)

        # Data
        categories = ["Apples", "Bananas", "Cherries", "Dates", "Elderberries"]
        values = np.array([12, 23, 36, 18, 29])

        # Bar chart
        bar = pg.BarGraphItem(
            x=np.arange(len(categories)),  # x positions
            height=values,
            width=0.6,
            brush="skyblue"
        )

        plot = pg.PlotWidget()
        plot.addItem(bar)

        # Customize look
        plot.setBackground("w")
        plot.setTitle("Fruit Counts", color="k", size="14pt")
        plot.showGrid(x=True, y=True)
        plot.setYRange(0, max(values) + 5)

        # Set x-axis ticks to category names
        axis = plot.getAxis("bottom")
        axis.setTicks([list(enumerate(categories))])

        layout.addWidget(plot)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
