import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import pydicom

from matplotlib.widgets import Slider

DICOM_FILE_NAME = '04RAND092.dcm'
SEGMENTATION_FILE_NAME = '04RAND092.dcm.seg.npy'
# File paths for demo Marcel and Bibi
DICOM_FILE_PATH = os.path.join('/Volumes/PHILIPS UFD/marcelvdpoll/original', DICOM_FILE_NAME)
SEGMENTATION_FILE_PATH = os.path.join('/Volumes/PHILIPS UFD/marcelvdpoll/output/defaultpipeline/segmentmusclefatl3tensorflowtask', SEGMENTATION_FILE_NAME)
# DICOM_FILE_PATH = f'/Users/ralph/Library/CloudStorage/GoogleDrive-ralph.brecheisen@gmail.com/My Drive/data/mosamatic2/data/l3_edema/{DICOM_FILE_NAME}'
# if sys.platform.startswith('win'):
#     DICOM_FILE_PATH = f'G:\\My Drive\\data\\mosamatic2\\data\\l3_edema\\{DICOM_FILE_NAME}'
# SEGMENTATION_FILE_PATH = f'/Users/ralph/Library/CloudStorage/GoogleDrive-ralph.brecheisen@gmail.com/My Drive/data/mosamatic2/data/l3_edema/{SEGMENTATION_FILE_NAME}'
# if sys.platform.startswith('win'):
#     SEGMENTATION_FILE_PATH = f'G:\\My Drive\\data\\mosamatic2\\data\\l3_edema\\{SEGMENTATION_FILE_NAME}'

HU_MIN = -29
HU_MAX = 150

slider_lo_ax = None
slider_hi_ax = None
slider_lo = None
slider_hi = None
image = None
muscle_mask = None
hu_lo = 30
hu_hi = 150
fig = None
axes = None
slider_lo_text = None
slider_hi_text = None


def rgba_from_binary_mask(mask, rgba, alpha):
    out = np.zeros((*mask.shape, 4), dtype=np.float32)
    out[mask] = (rgba[0], rgba[1], rgba[2], alpha)
    return out


def rgba_from_binary_mask_thresholded(image, mask, label, hu_lo, hu_hi, alpha):
    mask = (mask == label)
    red = mask & (image >= hu_lo) & (image <= hu_hi)
    yellow = mask & (image < hu_lo)
    overlay = np.zeros((*image.shape, 4), dtype=np.float32)
    overlay[red] = (1.0, 0.0, 0.0, alpha)
    overlay[yellow] = (1.0, 1.0, 0.0, alpha)
    return overlay


def on_change_lo(value):
    axes[1].clear()
    axes[1].imshow(apply_window_and_level(image), cmap="gray")
    axes[1].imshow(rgba_from_binary_mask_thresholded(image, muscle_mask, label=1, hu_lo=value, hu_hi=hu_hi, alpha=1))
    axes[1].axis("off")
    axes[1].set_title(f"Muscle low-RA (yellow) and high-RA (red)")
    fig.canvas.draw_idle()


def on_change_hi(value):
    axes[1].clear()
    axes[1].imshow(apply_window_and_level(image), cmap="gray")
    axes[1].imshow(rgba_from_binary_mask_thresholded(image, muscle_mask, label=1, hu_lo=hu_lo, hu_hi=value, alpha=1))
    axes[1].axis("off")
    axes[1].set_title(f"Muscle low-RA (yellow) and high-RA (red)")
    fig.canvas.draw_idle()


def apply_window_and_level(img, window=400, level=50):
    lo = level - window / 2.0
    hi = level + window / 2.0
    img = np.clip(img, lo, hi)
    img = (img - lo) / (hi - lo)          # -> 0..1
    return (img * 255.0 + 0.5)


def main():
    global fig, axes, image, muscle_mask, slider_lo, slider_lo_ax, slider_lo_text

    # Load image
    p = pydicom.dcmread(DICOM_FILE_PATH)
    image = p.pixel_array.astype(np.float32)
    image = image * float(getattr(p, "RescaleSlope", 1.0)) + float(getattr(p, "RescaleIntercept", 0.0))

    # Load segmentation mask
    mask = np.load(SEGMENTATION_FILE_PATH).astype(np.uint8)
    
    muscle_mask = (mask == 1)
    overlay_muscle = rgba_from_binary_mask(muscle_mask, rgba=(1.0, 0.0, 0.0), alpha=1)
    overlay_myosteatosis = rgba_from_binary_mask_thresholded(image, muscle_mask, label=1, hu_lo=hu_lo, hu_hi=hu_hi, alpha=1)

    # Create plots
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))    
    axes[0].imshow(apply_window_and_level(image), cmap='gray')
    axes[0].imshow(overlay_muscle)
    axes[0].axis("off")
    axes[0].set_title('Muscle (red)')
    axes[1].imshow(apply_window_and_level(image), cmap="gray")
    axes[1].imshow(overlay_myosteatosis)
    axes[1].axis("off")
    axes[1].set_title(f"Muscle low-RA (yellow) and high-RA (red)")

    # Create sliders for low and high thresholds
    slider_lo_ax = fig.add_axes([0.15, 0.06, 0.7, 0.03])
    slider_lo = Slider(slider_lo_ax, "Low-RA", HU_MIN, HU_MAX, valinit=hu_lo)
    slider_lo.on_changed(on_change_lo)
    slider_hi_ax = fig.add_axes([0.15, 0.03, 0.7, 0.03])
    slider_hi = Slider(slider_hi_ax, "High-RA", HU_MIN, HU_MAX, valinit=hu_hi)
    slider_hi.on_changed(on_change_hi)

    plt.show()


if __name__ == "__main__":
    main()