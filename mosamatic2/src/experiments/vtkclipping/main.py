#!/usr/bin/env python3
"""
Interactive VTK resection-plane demo:

- Loads CT (.nii/.nii.gz) and a mask volume (e.g. liver).
- Shows the original mask surface (wireframe) + the "remaining" mask surface (solid).
- Lets you drag/rotate an interactive plane widget to simulate a resection plane.
- Updates remaining volume (mL) live.

Keys:
  f  -> flip kept side of the plane
  r  -> reset plane to image center (normal = +X)
  q/ESC -> quit
"""

import argparse
import vtk
from vtk.util.numpy_support import vtk_to_numpy


def read_nifti(path: str) -> vtk.vtkImageData:
    r = vtk.vtkNIFTIImageReader()
    r.SetFileName(path)
    r.Update()
    return r.GetOutput()


def binarize_mask(img: vtk.vtkImageData, threshold: float = 0.5) -> vtk.vtkImageData:
    t = vtk.vtkImageThreshold()
    t.SetInputData(img)
    t.ThresholdByLower(threshold)  # values >= threshold -> InValue
    t.SetInValue(1)
    t.SetOutValue(0)
    t.SetOutputScalarTypeToUnsignedChar()
    t.Update()
    return t.GetOutput()


def count_ones(mask01: vtk.vtkImageData) -> int:
    """
    Counts voxels == 1 via a tiny histogram (fast, avoids numpy copy of full volume).
    Requires mask values only in {0,1}.
    """
    acc = vtk.vtkImageAccumulate()
    acc.SetInputData(mask01)
    acc.SetComponentExtent(0, 1, 0, 0, 0, 0)   # histogram bins for 0 and 1
    acc.SetComponentOrigin(0, 0, 0)
    acc.SetComponentSpacing(1, 1, 1)
    acc.Update()

    hist = acc.GetOutput().GetPointData().GetScalars()
    counts = vtk_to_numpy(hist)  # length 2
    return int(counts[1]) if counts.size >= 2 else 0


def volume_ml_from_count(mask01: vtk.vtkImageData, ones: int) -> float:
    sx, sy, sz = mask01.GetSpacing()  # typically mm
    voxel_vol_mm3 = float(sx * sy * sz)
    return (ones * voxel_vol_mm3) / 1000.0  # 1 mL = 1000 mm^3


def make_surface_actor(mask01: vtk.vtkImageData, iso: float = 0.5) -> tuple[vtk.vtkActor, vtk.vtkAlgorithm]:
    """
    Returns (actor, surface_extractor_filter)
    """
    # FlyingEdges3D is generally faster than MarchingCubes.
    surf = vtk.vtkFlyingEdges3D()
    surf.SetInputData(mask01)
    surf.SetValue(0, iso)
    surf.ComputeNormalsOn()
    surf.Update()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(surf.GetOutputPort())
    mapper.ScalarVisibilityOff()

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    return actor, surf


def main():
    ct = read_nifti("D:\\Mosamatic\\TotalSegmentator\\patient1.nii.gz")
    mask = read_nifti("D:\\Mosamatic\\TotalSegmentator\\output\\liver.nii.gz")
    mask01 = binarize_mask(mask, threshold=0.5)

    # Precompute total volume once
    total_ones = count_ones(mask01)
    total_ml = volume_ml_from_count(mask01, total_ones)

    # --- Clipping pipeline (mask01 -> stencil -> clipped_mask01) ---
    keep_negative_halfspace = {"value": True}  # mutable for callbacks

    clip_plane = vtk.vtkPlane()  # implicit function used by stencil
    bounds = mask01.GetBounds()
    cx = 0.5 * (bounds[0] + bounds[1])
    cy = 0.5 * (bounds[2] + bounds[3])
    cz = 0.5 * (bounds[4] + bounds[5])
    clip_plane.SetOrigin(cx, cy, cz)
    clip_plane.SetNormal(1, 0, 0)

    to_stencil = vtk.vtkImplicitFunctionToImageStencil()
    to_stencil.SetInput(clip_plane)
    to_stencil.SetOutputOrigin(mask01.GetOrigin())
    to_stencil.SetOutputSpacing(mask01.GetSpacing())
    to_stencil.SetOutputWholeExtent(mask01.GetExtent())
    to_stencil.Update()

    stencil = vtk.vtkImageStencil()
    stencil.SetInputData(mask01)
    stencil.SetStencilConnection(to_stencil.GetOutputPort())
    stencil.SetBackgroundValue(0)
    stencil.ReverseStencilOff()  # keep plane(x) <= 0 by default
    stencil.Update()

    clipped_mask01 = stencil.GetOutput()

    # --- Actors (original + remaining) ---
    original_actor, _orig_surf = make_surface_actor(mask01)
    original_actor.GetProperty().SetRepresentationToWireframe()
    original_actor.GetProperty().SetLineWidth(2.0)
    original_actor.GetProperty().SetOpacity(0.35)

    remaining_actor = vtk.vtkActor()
    remaining_surf = vtk.vtkFlyingEdges3D()
    remaining_surf.SetInputConnection(stencil.GetOutputPort())  # live connection
    remaining_surf.SetValue(0, 0.5)
    remaining_surf.ComputeNormalsOn()
    remaining_surf.Update()

    remaining_mapper = vtk.vtkPolyDataMapper()
    remaining_mapper.SetInputConnection(remaining_surf.GetOutputPort())
    remaining_mapper.ScalarVisibilityOff()

    remaining_actor.SetMapper(remaining_mapper)
    remaining_actor.GetProperty().SetOpacity(1.0)

    # --- Text overlay ---
    text = vtk.vtkTextActor()
    text.GetTextProperty().SetFontSize(18)
    text.GetTextProperty().SetColor(1, 1, 1)
    text.SetDisplayPosition(15, 15)

    def update_text():
        rem_ones = count_ones(clipped_mask01)
        rem_ml = volume_ml_from_count(mask01, rem_ones)
        res_ml = max(total_ml - rem_ml, 0.0)
        side = "keep plane(x) <= 0" if keep_negative_halfspace["value"] else "keep plane(x) > 0"
        text.SetInput(
            f"Total: {total_ml:.1f} mL\n"
            f"Remaining: {rem_ml:.1f} mL\n"
            f"Resected: {res_ml:.1f} mL\n"
            f"[f] flip side ({side})"
        )

    update_text()

    # --- Renderer / window / interactor ---
    ren = vtk.vtkRenderer()
    ren.AddActor(original_actor)
    ren.AddActor(remaining_actor)
    ren.AddActor2D(text)
    ren.SetBackground(0.08, 0.09, 0.11)

    rw = vtk.vtkRenderWindow()
    rw.SetWindowName("VTK Resection Plane Volume Demo")
    rw.SetSize(1200, 800)
    rw.AddRenderer(ren)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(rw)

    style = vtk.vtkInteractorStyleTrackballCamera()
    iren.SetInteractorStyle(style)

    # --- Interactive plane widget ---
    rep = vtk.vtkImplicitPlaneRepresentation()
    rep.SetPlaceFactor(1.0)
    rep.PlaceWidget(bounds)
    rep.SetNormal(1, 0, 0)
    rep.SetOrigin(cx, cy, cz)

    plane_widget = vtk.vtkImplicitPlaneWidget2()
    plane_widget.SetInteractor(iren)
    plane_widget.SetRepresentation(rep)
    plane_widget.SetEnabled(1)

    def apply_plane_from_widget():
        # Pull current plane from the widget and copy into our implicit function
        p = vtk.vtkPlane()
        rep.GetPlane(p)
        clip_plane.SetOrigin(p.GetOrigin())
        clip_plane.SetNormal(p.GetNormal())

        # Update which side we keep
        if keep_negative_halfspace["value"]:
            stencil.ReverseStencilOff()  # keep implicit<=0
        else:
            stencil.ReverseStencilOn()   # keep implicit>0

        # Force pipeline refresh
        to_stencil.Modified()
        stencil.Modified()
        stencil.Update()

        update_text()
        rw.Render()

    def on_plane_interaction(_obj, _evt):
        apply_plane_from_widget()

    plane_widget.AddObserver(vtk.vtkCommand.InteractionEvent, on_plane_interaction)
    plane_widget.AddObserver(vtk.vtkCommand.EndInteractionEvent, on_plane_interaction)

    # --- Key bindings ---
    def on_keypress(_obj, _evt):
        key = iren.GetKeySym().lower()
        if key == "f":
            keep_negative_halfspace["value"] = not keep_negative_halfspace["value"]
            apply_plane_from_widget()
        elif key == "r":
            rep.SetOrigin(cx, cy, cz)
            rep.SetNormal(1, 0, 0)
            apply_plane_from_widget()

    iren.AddObserver("KeyPressEvent", on_keypress)

    # Camera setup
    ren.ResetCamera()
    rw.Render()
    iren.Initialize()
    iren.Start()


if __name__ == "__main__":
    main()
