


# class NiftiSliceViewer2(QWidget):
#     def __init__(self):
#         super(NiftiSliceViewer, self).__init__()
#         self._nifti_file = None
#         self._interactor_style = None
#         self._render_window_interactor = None
#         self._render_window = None
#         self._interactor = None
#         self._view_orientation = None
#         self._image_viewer = None
#         self._renderer = None
#         self._image_reslicer = None
#         self._slice_text_actor = None
#         self._usage_text_actor = None
#         self._reader = None
#         self._shift_scale = None
#         self._colors = None
#         self.init_layout()

#     # LAYOUT

#     def init_layout(self):
#         layout = QVBoxLayout()
#         layout.addWidget(self.render_window_interactor())
#         self.setLayout(layout)

#     # GETTERS/SETTERS

#     def nifti_file(self):
#         return self._nifti_file
    
#     def set_nifti_file(self, nifti_file):
#         self._nifti_file = nifti_file

#     def interactor_style(self):
#         if not self._interactor_style:
#             self._interactor_style = CustomInteractorStyle(self.image_viewer(), self.slice_text_actor())
#         return self._interactor_style
    
#     def render_window_interactor(self):
#         if not self._render_window_interactor:
#             self._render_window_interactor = QVTKRenderWindowInteractor()
#             self._render_window_interactor.SetInteractorStyle(self.interactor_style())
#         return self._render_window_interactor
    
#     def render_window(self):
#         if not self._render_window:
#             self._render_window = self.render_window_interactor().GetRenderWindow()
#         return self._render_window
    
#     def interactor(self):
#         if not self._interactor:
#             self._interactor = self.render_window().GetInteractor()
#             self._interactor.SetInteractorStyle(self.interactor_style())
#         return self._interactor
    
#     def view_orientation(self):
#         return self._view_orientation
    
#     def set_view_orientation(self, view_orientation):
#         self._view_orientation = view_orientation

#     def renderer(self):
#         if not self._renderer:
#             self._renderer = None
#         return self._renderer

#     def image_viewer(self):
#         if not self._image_viewer:
#             self._image_viewer = vtk.vtkImageViewer2()
#             self._image_viewer.SetInputConnection(self.image_reslicer().GetOutputPort())
#             self._image_viewer.SetColorWindow(COLOR_WINDOW)   # like CT WW
#             self._image_viewer.SetColorLevel(COLOR_LEVEL)
#             self._image_viewer.SetupInteractor(self.interactor())
#         return self._image_viewer
    
#     def image_reslicer(self):
#         if not self._image_reslicer:
#             self._image_reslicer = vtk.vtkImageReslice()
#             self._image_reslicer.SetInputConnection(self.shift_scale().GetOutputPort())
#             # Set the output spacing to be 1, 1, 1. This is not strictly necessary but can be useful.
#             self._image_reslicer.SetOutputSpacing(1, 1, 1)
#             if self.view_orientation() == 'coronal':
#                 self._image_reslicer.SetResliceAxesDirectionCosines(1,0,0, 0,0,1, 0,-1,0)
#             elif self.view_orientation() == 'sagittal':
#                 self._image_reslicer.SetResliceAxesDirectionCosines(0,1,0, 0,0,1, 1,0,0)
#             else:
#                 # Default orientation: axial
#                 pass
#         return self._image_reslicer
    
#     def slice_text_actor(self):
#         if not self._slice_text_actor:
#             self._slice_text_actor = self.create_text_actor("", 15, 10, 20, align_bottom=True)
#         return self._slice_text_actor
    
#     def usage_text_actor(self):
#         if not self._usage_text_actor:
#             self.usage_text_actor = self.create_text_actor(
#                 "- Slice with mouse wheel or Up/Down-Key\n- Zoom with pressed right mouse button while dragging",
#                 0.05, 0.95, 14, normalized=True)
#         return self._usage_text_actor
    
#     def reader(self):
#         if not self._reader:
#             self._reader = vtk.vtkNIFTIImageReader()
#             self._reader.SetFileName(self.nifti_file())
#             self._reader.Update()
#         return self._reader
    
#     def shift_scale(self):
#         if not self._shift_scale:
#             self._shift_scale = vtk.vtkImageShiftScale()
#             self._shift_scale.SetInputConnection(self.reader().GetOutputPort())
#             self._shift_scale.SetShift(IMAGE_SHIFT_SCALE)
#             self._shift_scale.SetScale(1.0)
#             self._shift_scale.Update()
#         return self._shift_scale
    
#     def colors(self):
#         if not self._colors:
#             self._colors = vtk.vtkNamedColors()
#         return self._colors

#     def create_text_actor(self, text, x, y, font_size, align_bottom=False, normalized=False):
#         text_prop = vtk.vtkTextProperty()
#         text_prop.SetFontFamilyToCourier()
#         text_prop.SetFontSize(font_size)
#         text_prop.SetVerticalJustificationToBottom() if align_bottom else text_prop.SetVerticalJustificationToTop()
#         text_prop.SetJustificationToLeft()
#         text_mapper = vtk.vtkTextMapper()
#         text_mapper.SetInput(text)
#         text_mapper.SetTextProperty(text_prop)
#         text_actor = vtk.vtkActor2D()
#         text_actor.SetMapper(text_mapper)
#         if normalized:
#             text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
#         text_actor.SetPosition(x, y)
#         return text_actor

#     def update_status_message(self, message):
#         self.slice_text_actor().GetMapper().SetInput(message)

#     def render(self):
#         self.image_viewer().GetRenderer().AddActor2D(self.slice_text_actor())
#         self.image_viewer().GetRenderer().AddActor2D(self.usage_text_actor())
#         self.image_viewer().Render()
#         self.image_viewer().GetRenderer().ResetCamera()
#         self.image_viewer().GetRenderer().SetBackground(self.colors().GetColor3d('Black'))
#         self.image_viewer().GetRenderWindow().SetSize(800, 800)
#         self.image_viewer().GetRenderWindow().SetWindowName('NIFTI Viewer')
#         self.interactor().Initialize()


# import vtk
# # https://pycad.medium.com/dicom-viewer-in-python-5679a675a560


# class CustomInteractorStyle(vtk.vtkInteractorStyleImage):
#     def __init__(self, image_viewer, status_actor):
#         super().__init__()
#         self.AddObserver('MouseWheelForwardEvent', self.move_slice_forward)
#         self.AddObserver('MouseWheelBackwardEvent', self.move_slice_backward)
#         self.AddObserver('KeyPressEvent', self.key_press_event)
#         self._image_viewer = image_viewer
#         self._status_actor = status_actor
#         self._slice = image_viewer.GetSliceMin()
#         self._min_slice = image_viewer.GetSliceMin()
#         self._max_slice = image_viewer.GetSliceMax()
#         self.update_status_message()

#     def update_status_message(self):
#         # Update the status message with the current slice
#         message = f'Slice Number {self._slice + 1}/{self._max_slice + 1}'
#         self._status_actor.GetMapper().SetInput(message)

#     def move_slice_forward(self, obj, event):
#         if self._slice < self._max_slice:
#             self._slice += 1
#             self._image_viewer.SetSlice(self._slice)
#             self.update_status_message()
#             self._image_viewer.Render()

#     def move_slice_backward(self, obj, event):
#         if self._slice > self._min_slice:
#             self._slice -= 1
#             self._image_viewer.SetSlice(self._slice)
#             self.update_status_message()
#             self._image_viewer.Render()

#     def key_press_event(self, obj, event):
#         key = self.GetInteractor().GetKeySym()
#         if key == 'Up':
#             self.move_slice_forward(obj, event)
#         elif key == 'Down':
#             self.move_slice_backward(obj, event)
