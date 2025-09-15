import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFrame, QVBoxLayout, QWidget
from PySide6.QtCore import Qt

import vtk
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class VTKGraphWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Qt layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # VTK interactor widget
        self.vtkWidget = QVTKRenderWindowInteractor(self)
        layout.addWidget(self.vtkWidget)

        # Build a simple graph
        g = vtk.vtkMutableUndirectedGraph()
        v1 = g.AddVertex()
        v2 = g.AddVertex()
        v3 = g.AddVertex()
        v4 = g.AddVertex()
        g.AddEdge(v1, v2)
        g.AddEdge(v2, v3)
        g.AddEdge(v3, v4)
        g.AddEdge(v4, v1)
        g.AddEdge(v1, v3)  # cross edge

        # Layout & view
        self.view = vtk.vtkGraphLayoutView()
        self.view.AddRepresentationFromInput(g)
        self.view.SetLayoutStrategy("Force Directed")

        # Use the same render window
        self.view.SetRenderWindow(self.vtkWidget.GetRenderWindow())

        # Start interactor
        self.interactor = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.view.ResetCamera()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VTK Infovis Graph in PySide6")
        self.resize(800, 600)

        frame = QFrame()
        layout = QVBoxLayout()
        frame.setLayout(layout)

        # Add VTK graph widget
        self.graphWidget = VTKGraphWidget(self)
        layout.addWidget(self.graphWidget)

        self.setCentralWidget(frame)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    # Start VTK interactor loop
    window.graphWidget.interactor.Initialize()
    window.graphWidget.interactor.Start()

    sys.exit(app.exec())
