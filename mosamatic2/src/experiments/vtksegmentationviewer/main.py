import vtk
import sys
import pydicom
import numpy as np

from vtkmodules.util import numpy_support

DICOM_FILE_NAME = '04RAND092.dcm'
DICOM_FILE_PATH = f'/Users/ralph/Library/CloudStorage/GoogleDrive-ralph.brecheisen@gmail.com/My Drive/data/mosamatic2/data/l3_edema/{DICOM_FILE_NAME}'
SEGMENTATION_FILE_NAME = '04RAND092.dcm.seg.npy'
SEGMENTATION_FILE_PATH = f'/Users/ralph/Library/CloudStorage/GoogleDrive-ralph.brecheisen@gmail.com/My Drive/data/mosamatic2/data/l3_edema/{SEGMENTATION_FILE_NAME}'


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


def update_vtk_image_from_numpy(vtk_img, arr2d, vtk_type):
    h, w = arr2d.shape
    flat = np.ascontiguousarray(arr2d).ravel(order="C")
    vtk_arr = numpy_support.numpy_to_vtk(flat, deep=True, array_type=vtk_type)
    vtk_arr.SetName("scalars")
    vtk_img.SetDimensions(w, h, 1)
    vtk_img.GetPointData().SetScalars(vtk_arr)
    vtk_img.Modified()
    return vtk_img


def make_binary_rgba_overlay(binary_mask, rgba=(1,0,0,0.35)):
    """binary_mask is (H,W) uint8 {0,1}; returns vtkImageData RGBA."""
    vtk_mask = vtk.vtkImageData()
    update_vtk_image_from_numpy(vtk_mask, binary_mask.astype(np.uint8), vtk.VTK_UNSIGNED_CHAR)

    lut = vtk.vtkLookupTable()
    lut.SetNumberOfTableValues(2)
    lut.SetRange(0, 1)
    lut.Build()
    lut.SetTableValue(0, 0, 0, 0, 0)  # background transparent
    lut.SetTableValue(1, *rgba)

    mapper = vtk.vtkImageMapToColors()
    mapper.SetInputData(vtk_mask)
    mapper.SetLookupTable(lut)
    mapper.SetOutputFormatToRGBA()
    mapper.Update()

    # Return both: vtk_mask (so you can update it later) and mapper output port
    return vtk_mask, mapper


def get_lut(mask):
    lut = vtk.vtkLookupTable()
    max_label = int(mask.max())
    lut.SetNumberOfTableValues(max_label + 1)
    lut.SetRange(0, max_label)
    lut.Build()
    for i in range(max_label + 1):
        lut.SetTableValue(i, 0.0, 0.0, 0.0, 0.0)
    lut.SetTableValue(0, 0.0, 0.0, 0.0, 0.0)
    lut.SetTableValue(1, 1.0, 0.0, 0.0, 1.0)
    lut.SetTableValue(5, 1.0, 1.0, 0.0, 1.0)
    lut.SetTableValue(7, 0.0, 1.0, 1.0, 1.0)
    return lut


def main():

    L = 1
    alpha = 1.0
    threshold = 30

    # Load L3 image
    print('Loading image')
    p = pydicom.dcmread(DICOM_FILE_PATH)
    image = p.pixel_array.astype(np.float32)
    image = image * float(getattr(p, "RescaleSlope", 1.0)) + float(getattr(p, "RescaleIntercept", 0.0))
    image = np.flipud(image)
    # vtk_image = numpy_to_vtk_image(image, vtk.VTK_FLOAT)

    # Load segmentation mask
    print('Loading segmentation mask')
    mask = np.load(SEGMENTATION_FILE_PATH).astype(np.uint8)
    mask = np.flipud(mask)
    label_mask = (mask == L)
    hi = (label_mask & (image >= threshold)).astype(np.uint8)
    lo = (label_mask & (image <  threshold)).astype(np.uint8)
    vtk_hi_mask, hi_rgba = make_binary_rgba_overlay(hi, rgba=(1, 0, 1, alpha))
    vtk_lo_mask, lo_rgba = make_binary_rgba_overlay(lo, rgba=(1, 1, 0, alpha))
    # vtk_mask = numpy_to_vtk_image(mask, vtk.VTK_UNSIGNED_CHAR)

    # # Apply window/level to image
    # wl = vtk.vtkImageMapToWindowLevelColors()
    # wl.SetInputData(vtk_image)
    # wl.SetWindow(400.0)
    # wl.SetLevel(50.0)
    # wl.Update()

    # # Apply colors to mask
    # mask_rgba = vtk.vtkImageMapToColors()
    # mask_rgba.SetInputData(vtk_mask)
    # mask_rgba.SetLookupTable(get_lut(mask))
    # mask_rgba.SetOutputFormatToRGBA()
    # mask_rgba.Update()

    hi_actor = vtk.vtkImageActor()
    hi_actor.GetMapper().SetInputConnection(hi_rgba.GetOutputPort())
    hi_actor.PickableOff()

    lo_actor = vtk.vtkImageActor()
    lo_actor.GetMapper().SetInputConnection(lo_rgba.GetOutputPort())
    lo_actor.PickableOff()

    # # Create image actor
    # image_actor = vtk.vtkImageActor()
    # image_actor.GetMapper().SetInputConnection(wl.GetOutputPort())
    # image_actor.PickableOff()

    # # Create mask actor
    # mask_actor = vtk.vtkImageActor()
    # mask_actor.GetMapper().SetInputConnection(mask_rgba.GetOutputPort())

    # # Create blend between image and mask
    # blend = vtk.vtkImageBlend()
    # blend.AddInputConnection(wl.GetOutputPort())
    # blend.AddInputConnection(mask_rgba.GetOutputPort())
    # blend.SetOpacity(0, 1.0)  # base
    # blend.SetOpacity(1, 1.0)  # overlay (alpha comes from LUT)
    # blend.Update()

    # Create renderer
    ren = vtk.vtkRenderer()
    # ren.AddActor(image_actor)
    # ren.AddActor(mask_actor)
    ren.AddActor(hi_actor)
    ren.AddActor(lo_actor)
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