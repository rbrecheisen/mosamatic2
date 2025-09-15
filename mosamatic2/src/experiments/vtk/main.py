import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

import vtk


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Central widget and layout
        self.frame = QWidget()
        self.layout = QVBoxLayout()
        self.frame.setLayout(self.layout)
        self.setCentralWidget(self.frame)

        # Create VTK widget
        self.vtk_widget = QVTKRenderWindowInteractor(self.frame)
        self.layout.addWidget(self.vtk_widget)

        # VTK renderer and scene setup
        self.renderer = vtk.vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)

        # Add a simple 3D object
        cone = vtk.vtkConeSource()
        cone.SetHeight(3.0)
        cone.SetRadius(1.0)
        cone.SetResolution(30)

        cone_mapper = vtk.vtkPolyDataMapper()
        cone_mapper.SetInputConnection(cone.GetOutputPort())

        cone_actor = vtk.vtkActor()
        cone_actor.SetMapper(cone_mapper)

        self.renderer.AddActor(cone_actor)
        self.renderer.SetBackground(0.1, 0.2, 0.4)

        # Initialize interactor
        self.interactor = self.vtk_widget.GetRenderWindow().GetInteractor()
        self.interactor.Initialize()
        self.interactor.Start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
