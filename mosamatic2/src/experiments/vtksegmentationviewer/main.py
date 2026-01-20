import vtk
import pydicom
import numpy as np

from vtkmodules.util import numpy_support

DICOM_FILE_PATH = "M:\\data\\marcelvdpoll\\l3_edema\\original\\04RAND092.dcm"
SEGMENTATION_FILE_PATH = "M:\\data\\marcelvdpoll\\l3_edema\\output\\defaultpipeline\\segmentmusclefatl3tensorflowtask\\04RAND092.dcm.seg.npy"


def numpy_to_vtk_image(arr2d, vtk_scalar_type):
    h, w = arr2d.shape
    vtk_arr = numpy_support.numpy_to_vtk(
        num_array=np.ascontiguousarray(arr2d).ravel(order="C"),
        deep=True,
        array_type=vtk_scalar_type,
    )
    img = vtk.vtkImageData()
    img.SetDimensions(w, h, 1)
    img.GetPointData().SetScalars(vtk_arr)
    return img


def get_lut(mask):
    lut = vtk.vtkLookupTable()
    max_label = int(mask.max())
    lut.SetNumberOfTableValues(max_label + 1)
    lut.Build()
    lut.SetTableValue(0, 0.0, 0.0, 0.0, 0.0)
    default_colors = [
        (1.0, 0.0, 0.0, 0.35),  # red
        (0.0, 1.0, 0.0, 0.35),  # green
        (0.0, 0.6, 1.0, 0.35),  # blue-ish
        (1.0, 1.0, 0.0, 0.35),  # yellow
        (1.0, 0.0, 1.0, 0.35),  # magenta
        (0.0, 1.0, 1.0, 0.35),  # cyan
    ]
    for lab in range(1, max_label + 1):
        r, g, b, a = default_colors[(lab - 1) % len(default_colors)]
        lut.SetTableValue(lab, r, g, b, a)
    return lut


def main():

    # Load L3 image
    print('Loading image')
    p = pydicom.dcmread(DICOM_FILE_PATH)
    image = p.pixel_array.astype(np.float32)
    image = image * float(getattr(p, "RescaleSlope", 1.0)) + float(getattr(p, "RescaleIntercept", 0.0))
    image = np.flipud(image)
    vtk_image = numpy_to_vtk_image(image, vtk.VTK_FLOAT)

    # Load segmentation mask
    print('Loading segmentation mask')
    mask = np.load(SEGMENTATION_FILE_PATH).astype(np.uint8)
    mask = np.flipud(mask)
    vtk_mask = numpy_to_vtk_image(mask, vtk.VTK_UNSIGNED_CHAR)

    # Apply window/level to image
    wl = vtk.vtkImageMapToWindowLevelColors()
    wl.SetInputData(vtk_image)
    wl.SetWindow(400.0)
    wl.SetLevel(50.0)
    wl.Update()

    # Apply colors to mask
    mask_rgba = vtk.vtkImageMapToColors()
    mask_rgba.SetInputData(vtk_mask)
    mask_rgba.SetLookupTable(get_lut(mask))
    mask_rgba.SetOutputFormatToRGBA()
    mask_rgba.Update()

    # Create image actor
    image_actor = vtk.vtkImageActor()
    image_actor.GetMapper().SetInputConnection(wl.GetOutputPort())

    # Create mask actor
    mask_actor = vtk.vtkImageActor()
    mask_actor.GetMapper().SetInputConnection(mask_rgba.GetOutputPort())

    # # Create blend between image and mask
    # blend = vtk.vtkImageBlend()
    # blend.AddInputConnection(wl.GetOutputPort())
    # blend.AddInputConnection(mask_rgba.GetOutputPort())
    # blend.SetOpacity(0, 1.0)  # base
    # blend.SetOpacity(1, 1.0)  # overlay (alpha comes from LUT)
    # blend.Update()

    # Create renderer
    ren = vtk.vtkRenderer()
    ren.AddActor(image_actor)
    ren.AddActor(mask_actor)
    ren.GetActiveCamera().ParallelProjectionOn()
    ren.ResetCamera()

    # Create render window
    renwin = vtk.vtkRenderWindow()
    renwin.AddRenderer(ren)
    renwin.SetSize(900, 900)

    # Create render window interactor
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetInteractorStyle(vtk.vtkInteractorStyleImage())
    iren.SetRenderWindow(renwin)

    # # Create 2D image viewer
    # viewer = vtk.vtkImageViewer2()
    # viewer.SetInputConnection(blend.GetOutputPort())
    # viewer.SetupInteractor(iren)
    # viewer.GetRenderWindow().SetSize(900, 900)
    # viewer.Render()

    renwin.Render()
    iren.Start()


if __name__ == '__main__':
    main()