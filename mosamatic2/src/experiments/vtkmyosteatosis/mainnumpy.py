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


def label_mask_to_rgba(mask: np.ndarray, alpha: float = 0.35) -> np.ndarray:
    """
    mask: (H,W) with labels {0,1,5,7}
    returns RGBA float image (H,W,4) in [0..1]
    """
    h, w = mask.shape
    rgba = np.zeros((h, w, 4), dtype=np.float32)

    # background=0 => already transparent

    # muscle=1 => red
    m = (mask == 1)
    rgba[m] = (1.0, 0.0, 0.0, alpha)

    # visceral fat=5 => yellow
    v = (mask == 5)
    rgba[v] = (1.0, 1.0, 0.0, alpha)

    # subcutaneous fat=7 => cyan
    s = (mask == 7)
    rgba[s] = (0.0, 1.0, 1.0, alpha)

    return rgba


def show_ct_with_overlay(dicom_path: str, mask_npy_path: str,
                         window: float = 400, level: float = 40,
                         alpha: float = 0.35, flipud: bool = False):
    hu = load_ct_hu(dicom_path)
    mask = np.load(mask_npy_path)

    if mask.shape != hu.shape:
        raise ValueError(f"Shape mismatch: CT {hu.shape} vs mask {mask.shape}")

    print("Unique labels:", np.unique(mask).tolist())

    if flipud:
        hu = np.flipud(hu)
        mask = np.flipud(mask)

    hu_w = window_image(hu, window, level)
    overlay = label_mask_to_rgba(mask, alpha=alpha)

    plt.figure(figsize=(8, 8))
    plt.imshow(hu_w, cmap="gray")
    plt.imshow(overlay)  # RGBA overlay
    plt.axis("off")
    plt.title(f"CT (W/L={window}/{level}) + segmentation overlay")
    plt.show()


# Example usage:
show_ct_with_overlay(
    "D:\\Mosamatic\\MartijnBroen\\02-10-2025_twee_plaatjes\\org\\419474.dcm", 
    "D:\\Mosamatic\\MartijnBroen\\02-10-2025_twee_plaatjes\\defaultpipeline\\segmentmusclefatl3tensorflowtask\\419474.dcm.seg.npy", 
    window=400, 
    level=50, 
    alpha=1
)
