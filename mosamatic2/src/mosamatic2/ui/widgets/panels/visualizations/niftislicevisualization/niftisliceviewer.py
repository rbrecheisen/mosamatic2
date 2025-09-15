import vtk


class CustomInteractorStyle(vtk.vtkInteractorStyleImage):
    def __init__(self, image_viewer, status_actor):
        super().__init__()
        self.AddObserver('MouseWheelForwardEvent', self.move_slice_forward)
        self.AddObserver('MouseWheelBackwardEvent', self.move_slice_backward)
        self.AddObserver('KeyPressEvent', self.key_press_event)
        self.image_viewer = image_viewer
        self.status_actor = status_actor
        self.slice = image_viewer.GetSliceMin()
        self.min_slice = image_viewer.GetSliceMin()
        self.max_slice = image_viewer.GetSliceMax()
        self.update_status_message()

    def update_status_message(self):
        # Update the status message with the current slice
        message = f'Slice Number {self.slice + 1}/{self.max_slice + 1}'
        self.status_actor.GetMapper().SetInput(message)

    def move_slice_forward(self, obj, event):
        if self.slice < self.max_slice:
            self.slice += 1
            self.image_viewer.SetSlice(self.slice)
            self.update_status_message()
            self.image_viewer.Render()

    def move_slice_backward(self, obj, event):
        if self.slice > self.min_slice:
            self.slice -= 1
            self.image_viewer.SetSlice(self.slice)
            self.update_status_message()
            self.image_viewer.Render()

    def key_press_event(self, obj, event):
        key = self.GetInteractor().GetKeySym()
        if key == 'Up':
            self.move_slice_forward(obj, event)
        elif key == 'Down':
            self.move_slice_backward(obj, event)


class NiftiSliceViewer:
    def __init__(self, nifti_file, view_orientation='axial'):
        self.nifti_file = nifti_file
        self.view_orientation = view_orientation  # New attribute for view orientation
        self.reader = None
        self.shifted_data = None
        self.colors = vtk.vtkNamedColors()
        self.setup_reader()
        self.setup_data_shift()
        self.setup_reslice()  # Call setup_reslice instead of setup_viewer directly
        self.setup_text_labels()
        self.configure_interactor()

    def setup_reader(self):
        self.reader = vtk.vtkNIFTIImageReader()
        self.reader.SetFileName(self.nifti_file)
        self.reader.Update()

    def setup_data_shift(self):
        self.shifted_data = vtk.vtkImageShiftScale()
        self.shifted_data.SetInputConnection(self.reader.GetOutputPort())
        self.shifted_data.SetShift(-1000)
        self.shifted_data.SetScale(1.0)
        self.shifted_data.Update()

    def setup_reslice(self):
        self.reslice = vtk.vtkImageReslice()
        self.reslice.SetInputConnection(self.shifted_data.GetOutputPort())

        # Set the output spacing to be 1, 1, 1. This is not strictly necessary but can be useful.
        self.reslice.SetOutputSpacing(1, 1, 1)

        if self.view_orientation == 'coronal':
            self.reslice.SetResliceAxesDirectionCosines(1,0,0, 0,0,1, 0,-1,0)
        elif self.view_orientation == 'sagittal':
            self.reslice.SetResliceAxesDirectionCosines(0,1,0, 0,0,1, 1,0,0)
        # Default is axial; no changes needed

        self.setup_viewer()

    def setup_viewer(self):
        self.image_viewer = vtk.vtkImageViewer2()
        self.image_viewer.SetInputConnection(self.reslice.GetOutputPort())
        self.image_viewer.SetColorWindow(500)   # like CT WW
        self.image_viewer.SetColorLevel(50)
        # Rest of the setup_viewer method remains unchanged


    def setup_text_labels(self):
        self.slice_text_actor = self.create_text_actor("", 15, 10, 20, align_bottom=True)
        self.usage_text_actor = self.create_text_actor(
            "- Slice with mouse wheel or Up/Down-Key\n- Zoom with pressed right mouse button while dragging",
            0.05, 0.95, 14, normalized=True)

    def configure_interactor(self):
        self.interactor = vtk.vtkRenderWindowInteractor()
        self.interactor_style = CustomInteractorStyle(self.image_viewer, self.slice_text_actor)
        self.image_viewer.SetupInteractor(self.interactor)
        self.interactor.SetInteractorStyle(self.interactor_style)

    def create_text_actor(self, text, x, y, font_size, align_bottom=False, normalized=False):
        text_prop = vtk.vtkTextProperty()
        text_prop.SetFontFamilyToCourier()
        text_prop.SetFontSize(font_size)
        text_prop.SetVerticalJustificationToBottom() if align_bottom else text_prop.SetVerticalJustificationToTop()
        text_prop.SetJustificationToLeft()

        text_mapper = vtk.vtkTextMapper()
        text_mapper.SetInput(text)
        text_mapper.SetTextProperty(text_prop)

        text_actor = vtk.vtkActor2D()
        text_actor.SetMapper(text_mapper)
        if normalized:
            text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
        text_actor.SetPosition(x, y)

        return text_actor

    def update_status_message(self, message):
        self.slice_text_actor.GetMapper().SetInput(message)

    def render(self):
        self.image_viewer.GetRenderer().AddActor2D(self.slice_text_actor)
        self.image_viewer.GetRenderer().AddActor2D(self.usage_text_actor)
        self.image_viewer.Render()
        self.image_viewer.GetRenderer().ResetCamera()
        self.image_viewer.GetRenderer().SetBackground(self.colors.GetColor3d('Black'))
        self.image_viewer.GetRenderWindow().SetSize(800, 800)
        self.image_viewer.GetRenderWindow().SetWindowName('NIFTI Viewer')
        self.interactor.Start()