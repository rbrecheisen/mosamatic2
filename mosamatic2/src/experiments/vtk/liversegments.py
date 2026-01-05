import os
import vtk
import platform
import pandas as pd

PLATFORM = platform.system()
if PLATFORM == 'Windows':
    BASE_DIR_PATH = 'G:/My Drive'
elif PLATFORM == 'Darwin':
    BASE_DIR_PATH = '/Users/ralph/Library/CloudStorage/GoogleDrive-ralph.brecheisen@gmail.com/My Drive'
SEGMENTS_DIR_PATH = f'{BASE_DIR_PATH}/data/mosamatic2/data/liveranalysispipeline/totalsegmentatortask'
SEGMENTS_STATISTICS_FILE_PATH = f'{BASE_DIR_PATH}/data/mosamatic2/data/liveranalysispipeline/calculatemaskstatisticstask/statistics.csv'

SEGMENT_COLORS = [
    (0.80, 0.25, 0.25),  # muted red
    (0.25, 0.55, 0.80),  # steel blue
    (0.30, 0.70, 0.45),  # green
    (0.85, 0.65, 0.25),  # amber
    (0.55, 0.40, 0.75),  # purple
    (0.90, 0.45, 0.15),  # orange
    (0.20, 0.75, 0.75),  # teal
    (0.75, 0.75, 0.30),  # olive
]

OPACITY_SELECTED = 1.0
OPACITY_NOT_SELECTED = 0.25


class MultiActorPicker:
    def __init__(self, renderer, interactor, actors, volumes):
        self.ren = renderer
        self.iren = interactor
        self.actors = actors
        self.actor_keys = {v: k for k, v in actors.items()}
        self.volumes = volumes
        self.selected = set()
        self._orig = {}

        self.picker = vtk.vtkCellPicker()
        self.picker.SetTolerance(0.001)

        # Use trackball so it rotates only when you move
        self.style = vtk.vtkInteractorStyleTrackballCamera()
        self.iren.SetInteractorStyle(self.style)

        # Hook events
        self.iren.AddObserver("LeftButtonPressEvent", self.on_left_down)
        self.iren.AddObserver("LeftButtonReleaseEvent", self.on_left_up)

        self._allow_camera_drag = True

    def _save(self, a):
        if a in self._orig:
            return

    def _highlight(self, a, on):
        self._save(a)
        p = a.GetProperty()
        if on:
            p.SetOpacity(OPACITY_SELECTED)
        else:
            p.SetOpacity(OPACITY_NOT_SELECTED)

    def clear(self):
        for a in list(self.selected):
            self._highlight(a, False)
        self.selected.clear()

    def toggle(self, a):
        if a in self.selected:
            self._highlight(a, False)
            self.selected.remove(a)
        else:
            self._highlight(a, True)
            self.selected.add(a)
        total_selected_volume = 0
        for a in self.selected:
            a_key = self.actor_keys[a]
            volume = int(self.volumes[a_key])
            total_selected_volume += volume
        print(f'total_selected_volume: {total_selected_volume}')
            

    def on_left_down(self, iren, evt):
        x, y = iren.GetEventPosition()

        # Only do picking when Shift or Ctrl is held.
        do_pick = (iren.GetShiftKey() or iren.GetControlKey())

        if do_pick:
            self.picker.Pick(x, y, 0, self.ren)
            a = self.picker.GetActor()
            a_key = self.actor_keys[a]

            if a in self.actors.values():
                # Additive (Shift/Ctrl): toggle selection
                self.toggle(a)
            else:
                # Shift/Ctrl + empty click: clear selection (optional)
                self.clear()

            iren.GetRenderWindow().Render()
            self._allow_camera_drag = False  # don't also start a camera drag
            return

        # No modifier => normal rotate/pan/zoom interaction
        self._allow_camera_drag = True
        self.style.OnLeftButtonDown()

    def on_left_up(self, iren, evt):
        if self._allow_camera_drag:
            self.style.OnLeftButtonUp()


def labelmap_to_surface(image: vtk.vtkImageData, label=1) -> vtk.vtkPolyData:
    dmc = vtk.vtkDiscreteMarchingCubes()
    dmc.SetInputData(image)
    dmc.SetValue(0, label)
    dmc.Update()
    cleaner = vtk.vtkCleanPolyData()
    cleaner.SetInputConnection(dmc.GetOutputPort())
    cleaner.Update()
    smoother = vtk.vtkWindowedSincPolyDataFilter()
    smoother.SetInputConnection(cleaner.GetOutputPort())
    smoother.SetNumberOfIterations(20)   # 10–30 typical
    smoother.SetPassBand(0.1)              # smaller = smoother (e.g. 0.05–0.2)
    smoother.SetFeatureAngle(120.0)      # preserve sharper edges
    smoother.BoundarySmoothingOff()              # usually best for closed organs
    smoother.FeatureEdgeSmoothingOff()           # keep features; turn On if you want more smoothing
    smoother.NonManifoldSmoothingOn()
    smoother.NormalizeCoordinatesOn()            # helps numerical stability
    smoother.Update()
    normals = vtk.vtkPolyDataNormals()
    normals.SetInputConnection(smoother.GetOutputPort())
    normals.SetComputePointNormals(True)
    normals.SetComputeCellNormals(False)
    normals.SetAutoOrientNormals(True)
    normals.SetConsistency(True)
    normals.Update()
    return normals.GetOutput()


def polydata_actor(polydata: vtk.vtkPolyData, opacity=1.0) -> vtk.vtkActor:
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polydata)
    mapper.ScalarVisibilityOff()
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    return actor


def build_liver_volume_dict(f_path):
    volumes = {}
    df = pd.read_csv(f_path, sep=';')
    for _, row in df.iterrows():
        volumes[row['file']] = row['volume_mL']
    return volumes


def main():
    liver_segments_dir_path = SEGMENTS_DIR_PATH
    liver_segments_stats_file_path = SEGMENTS_STATISTICS_FILE_PATH
    volumes = build_liver_volume_dict(liver_segments_stats_file_path)

    renderer = vtk.vtkRenderer()
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)
    interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())

    i = 0
    actors = {}
    for f in os.listdir(liver_segments_dir_path):
        segment_name = f
        f_path = os.path.join(liver_segments_dir_path, f)
        reader = vtk.vtkNIFTIImageReader()
        reader.SetFileName(f_path)
        reader.Update()
        image = reader.GetOutput()
        surface = labelmap_to_surface(image)
        actor = polydata_actor(surface, 1.0)
        prop = actor.GetProperty()
        prop.SetSpecular(0.3)
        prop.SetSpecularPower(20)
        prop.SetDiffuse(0.7)
        prop.SetAmbient(0.1)
        prop.SetColor(*SEGMENT_COLORS[i])
        prop.SetOpacity(0.5)
        renderer.AddActor(actor)
        actors[segment_name] = actor
        i += 1

    picker = MultiActorPicker(renderer, interactor, actors, volumes)

    renderer.SetBackground(0.1, 0.1, 0.12)
    renderer.ResetCamera()
    render_window.SetSize(1200, 900)
    render_window.Render()
    interactor.Start()


if __name__ == '__main__':
    main()