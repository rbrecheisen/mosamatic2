#!/usr/bin/env python3
"""
VTK overlay demo: single-slice CT (from ONE DICOM file) + multi-label segmentation mask (NumPy)
with a color map (LUT) for:
  background=0 (transparent)
  muscle=1 (red)
  visceral fat=5 (yellow)
  subcutaneous fat=7 (cyan)

Run:
  python vtk_l3_overlay_dicom_multilabel.py --dicom slice.dcm --mask seg.npy
"""

import argparse
import sys
import numpy as np
import vtk
from vtkmodules.util import numpy_support
import pydicom


def load_ct_dicom_as_hu(dicom_path: str):
    ds = pydicom.dcmread(dicom_path)

    px = ds.pixel_array.astype(np.float32)

    slope = float(getattr(ds, "RescaleSlope", 1.0))
    intercept = float(getattr(ds, "RescaleIntercept", 0.0))
    ct_hu = px * slope + intercept

    # DICOM PixelSpacing = [row_spacing, col_spacing]
    if hasattr(ds, "PixelSpacing") and len(ds.PixelSpacing) >= 2:
        row_spacing = float(ds.PixelSpacing[0])
        col_spacing = float(ds.PixelSpacing[1])
        spacing_xy = (col_spacing, row_spacing)  # VTK order: x=cols, y=rows
    else:
        spacing_xy = (1.0, 1.0)

    return ct_hu.astype(np.int16), spacing_xy


def numpy2vtk_image(img2d: np.ndarray, spacing=(1.0, 1.0, 1.0), origin=(0.0, 0.0, 0.0)) -> vtk.vtkImageData:
    if img2d.ndim != 2:
        raise ValueError(f"Expected 2D array (H,W), got shape {img2d.shape}")

    h, w = img2d.shape
    vtk_img = vtk.vtkImageData()
    vtk_img.SetDimensions(w, h, 1)
    vtk_img.SetSpacing(float(spacing[0]), float(spacing[1]), float(spacing[2]))
    vtk_img.SetOrigin(float(origin[0]), float(origin[1]), float(origin[2]))

    flat = np.ascontiguousarray(img2d).ravel(order="C")
    vtk_arr = numpy_support.numpy_to_vtk(flat, deep=True)
    vtk_img.GetPointData().SetScalars(vtk_arr)
    return vtk_img


def build_segmentation_lut(alpha_default: float = 0.35) -> vtk.vtkLookupTable:
    max_label = 7
    lut = vtk.vtkLookupTable()
    lut.SetNumberOfTableValues(max_label + 1)
    lut.Build()

    # Default: transparent for all labels
    for i in range(max_label + 1):
        lut.SetTableValue(i, 0.0, 0.0, 0.0, 0.0)

    # Specific labels
    lut.SetTableValue(0, 0.0, 0.0, 0.0, 0.0)  # background transparent
    lut.SetTableValue(1, 1.0, 0.0, 0.0, float(alpha_default))  # muscle = red
    lut.SetTableValue(5, 1.0, 1.0, 0.0, float(alpha_default))  # visceral fat = yellow
    lut.SetTableValue(7, 0.0, 1.0, 1.0, float(alpha_default))  # subcutaneous fat = cyan

    return lut


def show_ct_with_multilabel_overlay(
    ct2d: np.ndarray,
    seg2d: np.ndarray,
    *,
    spacing_xy=(1.0, 1.0),
    window: float = 400.0,
    level: float = 40.0,
    overlay_alpha: float = 0.35,
    flipud: bool = False,
):
    if ct2d.shape != seg2d.shape:
        raise ValueError(f"CT shape {ct2d.shape} != seg shape {seg2d.shape}")

    if flipud:
        ct2d = np.flipud(ct2d)
        seg2d = np.flipud(seg2d)

    # Convert to VTK images
    ct_vtk = numpy2vtk_image(ct2d.astype(np.int16, copy=False), spacing=(spacing_xy[0], spacing_xy[1], 1.0))
    seg_vtk = numpy2vtk_image(seg2d.astype(np.uint8, copy=False), spacing=(spacing_xy[0], spacing_xy[1], 1.0))

    # CT: window/level -> RGB
    wl = vtk.vtkImageMapToWindowLevelColors()
    wl.SetInputData(ct_vtk)
    wl.SetWindow(float(window))
    wl.SetLevel(float(level))
    wl.Update()

    ct_actor = vtk.vtkImageActor()
    ct_actor.GetMapper().SetInputConnection(wl.GetOutputPort())

    # Segmentation: LUT -> RGBA
    lut = build_segmentation_lut(alpha_default=overlay_alpha)

    seg_rgba = vtk.vtkImageMapToColors()
    seg_rgba.SetInputData(seg_vtk)
    seg_rgba.SetLookupTable(lut)
    seg_rgba.SetOutputFormatToRGBA()
    seg_rgba.Update()

    seg_actor = vtk.vtkImageActor()
    seg_actor.GetMapper().SetInputConnection(seg_rgba.GetOutputPort())

    # Render
    ren = vtk.vtkRenderer()
    ren.AddActor(ct_actor)
    ren.AddActor(seg_actor)
    ren.ResetCamera()

    rw = vtk.vtkRenderWindow()
    rw.AddRenderer(ren)
    rw.SetSize(900, 900)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(rw)
    iren.SetInteractorStyle(vtk.vtkInteractorStyleImage())

    rw.Render()
    iren.Start()


def main(argv=None):
    # p = argparse.ArgumentParser(description="VTK overlay: CT from single DICOM + mask from NumPy .npy")
    # p.add_argument("--dicom", required=True, help="Path to single CT DICOM slice file")
    # p.add_argument("--mask", required=True, help="Path to mask .npy (H,W)")
    # p.add_argument("--window", type=float, default=400.0)
    # p.add_argument("--level", type=float, default=40.0)
    # p.add_argument("--alpha", type=float, default=0.35)
    # p.add_argument("--flipud", action="store_true", help="Flip arrays vertically before display")
    # args = p.parse_args(argv)

    # ct_hu, spacing_xy = load_ct_dicom_as_hu(args.dicom)
    ct_hu, spacing_xy = load_ct_dicom_as_hu("D:\\Mosamatic\\MartijnBroen\\02-10-2025_twee_plaatjes\\org\\419474.dcm")
    # mask = np.load(args.mask)
    mask = np.load("D:\\Mosamatic\\MartijnBroen\\02-10-2025_twee_plaatjes\\defaultpipeline\\segmentmusclefatl3tensorflowtask\\419474.dcm.seg.npy")

    if mask.ndim != 2:
        raise ValueError(f"Mask must be 2D (H,W). Got shape {mask.shape}")

    # Sanity check sizes
    if mask.shape != ct_hu.shape:
        raise ValueError(
            f"Mask shape {mask.shape} does not match DICOM pixel array shape {ct_hu.shape}. "
            "Make sure the mask corresponds to this slice and has same (rows, cols)."
        )
    
    uniq = np.unique(mask)
    print(f"Unique labels in segmentation: {uniq.tolist()}")

    show_ct_with_multilabel_overlay(
        ct_hu,
        mask,
        spacing_xy=spacing_xy,
        window=400,
        level=50,
        overlay_alpha=1,
        flipud=True,
    )    


if __name__ == "__main__":
    main(sys.argv[1:])


