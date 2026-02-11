import pydicom
import numpy as np
from pathlib import Path
from typing import Tuple
from pydicom.multival import MultiValue
from PySide6.QtGui import (
    QImage,
)


#-------------------------------------------------------------------------------------------------------
def clamp(v: int, lo: int, hi: int) -> int:
    return lo if v < lo else hi if v > hi else v


#-------------------------------------------------------------------------------------------------------
def circle_brush(radius: int) -> np.ndarray:
    """Boolean (2r+1, 2r+1) circular kernel."""
    r = max(1, int(radius))
    yy, xx = np.ogrid[-r : r + 1, -r : r + 1]
    return (xx * xx + yy * yy) <= (r * r)


#-------------------------------------------------------------------------------------------------------
def np_u8_gray_to_qimage(gray: np.ndarray) -> QImage:
    """gray: (H, W) uint8 -> QImage Format_Grayscale8 (shares memory!)."""
    if gray.dtype != np.uint8 or gray.ndim != 2:
        raise ValueError("Expected uint8 (H,W)")
    h, w = gray.shape
    # Important: keep a reference to `gray` alive as long as QImage is used.
    return QImage(gray.data, w, h, int(gray.strides[0]), QImage.Format_Grayscale8)


#-------------------------------------------------------------------------------------------------------
def np_rgba_to_qimage(rgba: np.ndarray) -> QImage:
    """rgba: (H, W, 4) uint8 -> QImage Format_RGBA8888 (shares memory!)."""
    if rgba.dtype != np.uint8 or rgba.ndim != 3 or rgba.shape[2] != 4:
        raise ValueError("Expected uint8 (H,W,4)")
    h, w, _ = rgba.shape
    return QImage(rgba.data, w, h, int(rgba.strides[0]), QImage.Format_RGBA8888)


#-------------------------------------------------------------------------------------------------------
def dicom_to_image_and_u8_display(path: Path) -> Tuple[np.ndarray, np.ndarray, dict]:
    """
    Read DICOM single-frame image -> display uint8 (H,W).
    Returns (disp8, meta). This is just for visualization; you keep original as needed.
    """
    if pydicom is None:
        raise RuntimeError("pydicom not installed. `pip install pydicom`")

    ds = pydicom.dcmread(str(path))
    img = ds.pixel_array.astype(np.float32)

    slope = float(getattr(ds, "RescaleSlope", 1.0))
    intercept = float(getattr(ds, "RescaleIntercept", 0.0))
    img = img * slope + intercept

    # Window/level if present
    wc = getattr(ds, "WindowCenter", None)
    ww = getattr(ds, "WindowWidth", None)

    def _mv_first(x):
        if isinstance(x, MultiValue):
            return float(x[0])
        return float(x)

    if wc is not None and ww is not None:
        c = _mv_first(wc)
        w = _mv_first(ww)
        lo = c - (w / 2.0)
        hi = c + (w / 2.0)
    else:
        lo, hi = np.percentile(img, (1, 99))
        if hi <= lo:
            lo, hi = float(img.min()), float(img.max() + 1e-6)

    disp = np.clip((img - lo) / (hi - lo), 0.0, 1.0)
    disp8 = (disp * 255.0).astype(np.uint8)

    meta = {
        "SOPInstanceUID": getattr(ds, "SOPInstanceUID", ""),
        "SeriesInstanceUID": getattr(ds, "SeriesInstanceUID", ""),
        "StudyInstanceUID": getattr(ds, "StudyInstanceUID", ""),
        "PixelSpacing": [float(x) for x in getattr(ds, "PixelSpacing", [])] if hasattr(ds, "PixelSpacing") else [],
        "Shape": list(disp8.shape),
    }
    return img, disp8, meta