#!/usr/bin/env python3
"""
Show a CT slice (single DICOM) with an overlay computed from HU values *within the muscle region*:

- Red:    muscle pixels with 30 <= HU <= 50
- Yellow: muscle pixels with HU < 30
- Transparent elsewhere

Optionally also create (and save) a new labeled mask:
  0 = not muscle / background
  1 = muscle in-range (red)
  2 = muscle low (yellow)

Run:
  python hu_based_muscle_overlay.py --dicom slice.dcm --seg seg.npy
  python hu_based_muscle_overlay.py --dicom slice.dcm --seg seg.npy --save-mask new_mask.npy
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
import pydicom


def load_ct_hu(dicom_path: str) -> np.ndarray:
    ds = pydicom.dcmread(dicom_path)
    img = ds.pixel_array.astype(np.float32)

    slope = float(getattr(ds, "RescaleSlope", 1.0))
    intercept = float(getattr(ds, "RescaleIntercept", 0.0))
    hu = img * slope + intercept
    return hu


def window_image(hu: np.ndarray, window: float, level: float) -> np.ndarray:
    lo = level - window / 2.0
    hi = level + window / 2.0
    return np.clip(hu, lo, hi)


def build_hu_overlay_within_muscle(
    hu: np.ndarray,
    seg: np.ndarray,
    *,
    muscle_label: int = 1,
    hu_low_thresh: float = 30.0,
    hu_high_thresh: float = 50.0,
    alpha: float = 0.35,
):
    """
    Returns:
      overlay_rgba: (H,W,4) float32 in [0..1]
      new_mask:     (H,W) uint8 labels:
                     0 = not muscle/background
                     1 = muscle in [hu_low_thresh, hu_high_thresh]
                     2 = muscle < hu_low_thresh
    """
    if hu.shape != seg.shape:
        raise ValueError(f"Shape mismatch: HU {hu.shape} vs seg {seg.shape}")

    muscle = (seg == muscle_label)

    red = muscle & (hu >= hu_low_thresh) & (hu <= hu_high_thresh)
    yellow = muscle & (hu < hu_low_thresh)

    overlay = np.zeros((*hu.shape, 4), dtype=np.float32)
    overlay[red] = (1.0, 0.0, 0.0, alpha)       # red
    overlay[yellow] = (1.0, 1.0, 0.0, alpha)    # yellow

    new_mask = np.zeros(hu.shape, dtype=np.uint8)
    new_mask[red] = 1
    new_mask[yellow] = 2

    return overlay, new_mask


def overlay_from_binary(mask: np.ndarray, rgba, alpha: float) -> np.ndarray:
    """mask (H,W) bool -> overlay (H,W,4)"""
    out = np.zeros((*mask.shape, 4), dtype=np.float32)
    out[mask] = (rgba[0], rgba[1], rgba[2], alpha)
    return out


def overlay_hu_within_muscle(
    hu: np.ndarray,
    muscle_mask: np.ndarray,
    hu_low: float,
    hu_high: float,
    alpha: float,
) -> np.ndarray:
    """
    Returns RGBA overlay:
      - red for hu in [hu_low, hu_high]
      - yellow for hu < hu_low
      - transparent elsewhere
    """
    red = muscle_mask & (hu >= hu_low) & (hu <= hu_high)
    yellow = muscle_mask & (hu < hu_low)
    overlay = np.zeros((*hu.shape, 4), dtype=np.float32)
    overlay[red] = (1.0, 0.0, 0.0, alpha)
    overlay[yellow] = (1.0, 1.0, 0.0, alpha)
    return overlay


def main():
    # ap = argparse.ArgumentParser()
    # ap.add_argument("--dicom", required=True, help="Path to single CT DICOM slice")
    # ap.add_argument("--seg", required=True, help="Path to segmentation .npy (H,W); muscle label assumed 1")
    # ap.add_argument("--muscle-label", type=int, default=1, help="Label value for muscle in seg mask")
    # ap.add_argument("--window", type=float, default=400.0)
    # ap.add_argument("--level", type=float, default=40.0)
    # ap.add_argument("--alpha", type=float, default=0.35)
    # ap.add_argument("--hu-low", type=float, default=30.0, help="Low HU threshold (yellow below this)")
    # ap.add_argument("--hu-high", type=float, default=50.0, help="High HU threshold (red up to this)")
    # ap.add_argument("--flipud", action="store_true", help="Flip HU+seg vertically before display")
    # ap.add_argument("--save-mask", default=None, help="If set, save new labeled mask (.npy)")
    # args = ap.parse_args()

    hu = load_ct_hu("D:\\Mosamatic\\MartijnBroen\\02-10-2025_twee_plaatjes\\org\\419474.dcm")
    seg = np.load("D:\\Mosamatic\\MartijnBroen\\02-10-2025_twee_plaatjes\\defaultpipeline\\segmentmusclefatl3tensorflowtask\\419474.dcm.seg.npy")

    if seg.ndim != 2 or hu.ndim != 2:
        raise ValueError(f"Expected 2D arrays. Got hu.ndim={hu.ndim}, seg.ndim={seg.ndim}")
    if seg.shape != hu.shape:
        raise ValueError(f"Shape mismatch: CT {hu.shape} vs seg {seg.shape}")

    print("Unique labels in seg:", np.unique(seg).tolist())

    flipud = False

    if flipud:
        hu = np.flipud(hu)
        seg = np.flipud(seg)

    # overlay, new_mask = build_hu_overlay_within_muscle(
    #     hu,
    #     seg,
    #     muscle_label=1,
    #     hu_low_thresh=30,
    #     hu_high_thresh=60,
    #     alpha=1,
    # )

    # if save_mask:
    #     np.save(save_mask, new_mask)
    #     print(f"Saved new mask to: {args.save_mask}")
    #     print("New mask labels present:", np.unique(new_mask).tolist())

    # Display
    hu_w = window_image(hu, 400, 50)

    muscle_mask = (seg == 1)

    # Plot 1 overlay: pure muscle (red)
    overlay_muscle = overlay_from_binary(muscle_mask, rgba=(1.0, 0.0, 0.0), alpha=1)

    # Plot 2 overlay: HU-thresholded within muscle (red/yellow)
    overlay_hu = overlay_hu_within_muscle(
        hu=hu,
        muscle_mask=muscle_mask,
        hu_low=30,
        hu_high=100,
        alpha=1,
    )

    # plt.figure(figsize=(8, 8))
    # plt.imshow(hu_w, cmap="gray")
    # plt.imshow(overlay)  # RGBA overlay computed from HU thresholds within muscle
    # plt.axis("off")
    # plt.title(f"Muscle HU overlay: red={30}..{60}, yellow< {30}")
    # plt.show()

    fig, axes = plt.subplots(1, 2, figsize=(14, 7))

    axes[0].imshow(hu_w, cmap="gray")
    axes[0].imshow(overlay_muscle)
    axes[0].axis("off")
    axes[0].set_title("Muscle mask (red)")

    axes[1].imshow(hu_w, cmap="gray")
    axes[1].imshow(overlay_hu)
    axes[1].axis("off")
    axes[1].set_title(f"Muscle HU overlay: red={30}..{60}, yellow< {30}")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
