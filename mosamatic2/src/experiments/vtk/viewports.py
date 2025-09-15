import os
import sys
import vtk
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

DICOM_DIR = 'G:\\My Drive\\data\\Mosamatic\\testdata\\CT\\patient1'


class MultiStyleInteractor(vtk.vtkInteractorStyle):
    def __init__(self, slice_actors, image_data, ren_3d):
        super().__init__()
        self.slice_actors = slice_actors
        self.image_data = image_data
        self.ren_3d = ren_3d

        # delegate style for 3D
        self.trackball = vtk.vtkInteractorStyleTrackballCamera()

        # hook events manually
        self.AddObserver("MouseWheelForwardEvent", self.OnMouseWheelForward)
        self.AddObserver("MouseWheelBackwardEvent", self.OnMouseWheelBackward)
        self.AddObserver("LeftButtonPressEvent", self.OnLeftButtonDown)
        self.AddObserver("LeftButtonReleaseEvent", self.OnLeftButtonUp)

    def _get_renderer_at_position(self, x, y):
        rw = self.GetInteractor().GetRenderWindow()
        size = rw.GetSize()
        nx, ny = x / size[0], y / size[1]
        collection = rw.GetRenderers()
        collection.InitTraversal()
        for i in range(collection.GetNumberOfItems()):
            ren = collection.GetNextItem()
            xmin, ymin, xmax, ymax = ren.GetViewport()
            if xmin <= nx <= xmax and ymin <= ny <= ymax:
                return ren
        return None

    def _scroll_slice(self, renderer, step):
        entry = self.slice_actors[renderer]
        orientation = entry["orientation"]
        idx = entry["index"]
        dims = self.image_data.GetDimensions()

        if orientation == "axial":
            idx = min(max(idx + step, 0), dims[2] - 1)
            entry["actor"].SetDisplayExtent(0, dims[0]-1, 0, dims[1]-1, idx, idx)
        elif orientation == "sagittal":
            idx = min(max(idx + step, 0), dims[0] - 1)
            entry["actor"].SetDisplayExtent(idx, idx, 0, dims[1]-1, 0, dims[2]-1)
        elif orientation == "coronal":
            idx = min(max(idx + step, 0), dims[1] - 1)
            entry["actor"].SetDisplayExtent(0, dims[0]-1, idx, idx, 0, dims[2]-1)

        entry["index"] = idx
        self.GetInteractor().GetRenderWindow().Render()

    # --- Events ---
    def OnMouseWheelForward(self, obj=None, ev=None):
        x, y = self.GetInteractor().GetEventPosition()
        renderer = self._get_renderer_at_position(x, y)
        if renderer in self.slice_actors:
            self._scroll_slice(renderer, +1)
        elif renderer == self.ren_3d:
            self.trackball.SetInteractor(self.GetInteractor())
            self.trackball.OnMouseWheelForward()

    def OnMouseWheelBackward(self, obj=None, ev=None):
        x, y = self.GetInteractor().GetEventPosition()
        renderer = self._get_renderer_at_position(x, y)
        if renderer in self.slice_actors:
            self._scroll_slice(renderer, -1)
        elif renderer == self.ren_3d:
            self.trackball.SetInteractor(self.GetInteractor())
            self.trackball.OnMouseWheelBackward()

    def OnLeftButtonDown(self, obj=None, ev=None):
        x, y = self.GetInteractor().GetEventPosition()
        renderer = self._get_renderer_at_position(x, y)
        if renderer == self.ren_3d:
            self.trackball.SetInteractor(self.GetInteractor())
            self.trackball.OnLeftButtonDown()

    def OnLeftButtonUp(self, obj=None, ev=None):
        x, y = self.GetInteractor().GetEventPosition()
        renderer = self._get_renderer_at_position(x, y)
        if renderer == self.ren_3d:
            self.trackball.SetInteractor(self.GetInteractor())
            self.trackball.OnLeftButtonUp()


def create_slice_renderer(image_data, orientation, slice_index, viewport):
    dims = image_data.GetDimensions()

    slice_actor = vtk.vtkImageActor()
    mapper = slice_actor.GetMapper()
    mapper.SetInputData(image_data)

    if orientation == "axial":
        slice_actor.SetDisplayExtent(0, dims[0]-1, 0, dims[1]-1, slice_index, slice_index)
    elif orientation == "sagittal":
        slice_actor.SetDisplayExtent(slice_index, slice_index, 0, dims[1]-1, 0, dims[2]-1)
    elif orientation == "coronal":
        slice_actor.SetDisplayExtent(0, dims[0]-1, slice_index, slice_index, 0, dims[2]-1)

    ren = vtk.vtkRenderer()
    ren.AddActor(slice_actor)
    ren.SetViewport(*viewport)

    # Fix camera orientation
    cam = ren.GetActiveCamera()
    if orientation == "axial":
        cam.SetFocalPoint(dims[0]//2, dims[1]//2, slice_index)
        cam.SetPosition(dims[0]//2, dims[1]//2, slice_index + 500)
        cam.SetViewUp(0, -1, 0)
    elif orientation == "sagittal":
        cam.SetFocalPoint(slice_index, dims[1]//2, dims[2]//2)
        cam.SetPosition(slice_index + 500, dims[1]//2, dims[2]//2)
        cam.SetViewUp(0, 0, 1)
    elif orientation == "coronal":
        cam.SetFocalPoint(dims[0]//2, slice_index, dims[2]//2)
        cam.SetPosition(dims[0]//2, slice_index + 500, dims[2]//2)
        cam.SetViewUp(0, 0, 1)

    cam.ParallelProjectionOn()
    ren.ResetCamera()

    return ren, slice_actor


def create_volume_renderer(image_data, viewport):
    volume_mapper = vtk.vtkGPUVolumeRayCastMapper()
    volume_mapper.SetInputData(image_data)

    color = vtk.vtkColorTransferFunction()
    color.AddRGBPoint(0, 0.0, 0.0, 0.0)
    color.AddRGBPoint(500, 1.0, 0.5, 0.3)
    color.AddRGBPoint(1000, 1.0, 1.0, 0.9)

    opacity = vtk.vtkPiecewiseFunction()
    opacity.AddPoint(0, 0.0)
    opacity.AddPoint(500, 0.2)
    opacity.AddPoint(1000, 0.8)

    volume_property = vtk.vtkVolumeProperty()
    volume_property.SetColor(color)
    volume_property.SetScalarOpacity(opacity)
    volume_property.ShadeOn()
    volume_property.SetInterpolationTypeToLinear()

    volume = vtk.vtkVolume()
    volume.SetMapper(volume_mapper)
    volume.SetProperty(volume_property)

    ren = vtk.vtkRenderer()
    ren.AddVolume(volume)
    ren.SetViewport(*viewport)
    ren.ResetCamera()
    return ren


class MainWindow(QMainWindow):
    def __init__(self, image_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("VTK Slice + 3D Viewer with Scrolling - PySide6")

        frame = QWidget()
        layout = QVBoxLayout()
        frame.setLayout(layout)
        self.setCentralWidget(frame)

        vtk_widget = QVTKRenderWindowInteractor(frame)
        layout.addWidget(vtk_widget)

        render_window = vtk_widget.GetRenderWindow()
        interactor = render_window.GetInteractor()

        dims = image_data.GetDimensions()
        axial_index = dims[2] // 2
        sagittal_index = dims[0] // 2
        coronal_index = dims[1] // 2

        ren_axial, actor_axial = create_slice_renderer(image_data, "axial", axial_index, (0.0, 0.5, 0.5, 1.0))
        ren_sagittal, actor_sagittal = create_slice_renderer(image_data, "sagittal", sagittal_index, (0.5, 0.5, 1.0, 1.0))
        ren_coronal, actor_coronal = create_slice_renderer(image_data, "coronal", coronal_index, (0.0, 0.0, 0.5, 0.5))
        ren_3d = create_volume_renderer(image_data, (0.5, 0.0, 1.0, 0.5))

        render_window.AddRenderer(ren_axial)
        render_window.AddRenderer(ren_sagittal)
        render_window.AddRenderer(ren_coronal)
        render_window.AddRenderer(ren_3d)

        slice_actors = {
            ren_axial: {"actor": actor_axial, "orientation": "axial", "index": axial_index},
            ren_sagittal: {"actor": actor_sagittal, "orientation": "sagittal", "index": sagittal_index},
            ren_coronal: {"actor": actor_coronal, "orientation": "coronal", "index": coronal_index},
        }

        style = MultiStyleInteractor(slice_actors, image_data, ren_3d)
        interactor.SetInteractorStyle(style)
        interactor.Initialize()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    reader = vtk.vtkDICOMImageReader()
    reader.SetDirectoryName(DICOM_DIR)
    reader.Update()
    image_data = reader.GetOutput()
    window = MainWindow(image_data)
    window.show()
    sys.exit(app.exec())
