import pydicom
import pydicom.errors
import numpy as np
from pydicom.multival import MultiValue
from mosamatic2.core.managers.logmanager import LogManager

LOG = LogManager()


class DicomLoader:
    def __init__(self, file_path):
        self._file_path = file_path
        self._p = None
        self._slope = 1.0
        self._intercept = 0.0

    def load(self, stop_before_pixels=False):
        try:
            self._p = pydicom.dcmread(self._file_path, stop_before_pixels=stop_before_pixels)
            self._slope = float(getattr(self._p, "RescaleSlope", 1.0))
            self._intercept = float(getattr(self._p, "RescaleIntercept", 0.0))
            return True
        except pydicom.errors.InvalidDicomError as e:
            LOG.warning(f'File {self._file_path} is not a valid DICOM file ({e})')
            return False

    def load_as_numpy_and_u8disp(self):
        result = self.load()
        if not result:
            LOG.warning(f'Failed to load DICOM file')
            return None, None, None
        pixels = self._p.pixel_array
        pixels = pixels * self._slope + self._intercept

        # Window/level if present
        wc = getattr(self._p, "WindowCenter", None)
        ww = getattr(self._p, "WindowWidth", None)

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
            lo, hi = np.percentile(pixels, (1, 99))
            if hi <= lo:
                lo, hi = float(pixels.min()), float(pixels.max() + 1e-6)

        disp = np.clip((pixels - lo) / (hi - lo), 0.0, 1.0)
        disp8 = (disp * 255.0).astype(np.uint8)

        meta = {
            "SOPInstanceUID": getattr(self._p, "SOPInstanceUID", ""),
            "SeriesInstanceUID": getattr(self._p, "SeriesInstanceUID", ""),
            "StudyInstanceUID": getattr(self._p, "StudyInstanceUID", ""),
            "PixelSpacing": [float(x) for x in getattr(self._p, "PixelSpacing", [])] if hasattr(self._p, "PixelSpacing") else [],
            "Shape": list(disp8.shape),
        }
        return pixels, disp8, meta