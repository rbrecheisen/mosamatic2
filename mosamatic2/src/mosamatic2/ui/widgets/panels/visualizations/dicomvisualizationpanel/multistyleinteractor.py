import vtk


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
