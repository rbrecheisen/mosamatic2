import sys
import numpy as np
import matplotlib.pyplot as plt
import pydicom

from matplotlib.widgets import Slider

DICOM_FILE_NAME = '04RAND092.dcm'
DICOM_FILE_PATH = f'/Users/ralph/Library/CloudStorage/GoogleDrive-ralph.brecheisen@gmail.com/My Drive/data/mosamatic2/data/l3_edema/{DICOM_FILE_NAME}'
if sys.platform.startswith('win'):
    DICOM_FILE_PATH = f'G:\\My Drive\\data\\mosamatic2\\data\\l3_edema\\{DICOM_FILE_NAME}'
SEGMENTATION_FILE_NAME = '04RAND092.dcm.seg.npy'
SEGMENTATION_FILE_PATH = f'/Users/ralph/Library/CloudStorage/GoogleDrive-ralph.brecheisen@gmail.com/My Drive/data/mosamatic2/data/l3_edema/{SEGMENTATION_FILE_NAME}'
if sys.platform.startswith('win'):
    SEGMENTATION_FILE_PATH = f'G:\\My Drive\\data\\mosamatic2\\data\\l3_edema\\{SEGMENTATION_FILE_NAME}'

slider_ax = None
slider = None
image = None
muscle_mask = None
hu_lo = 30
hu_hi = 150
fig = None
axes = None
slider_value = None


def rgba_from_binary_mask(mask, rgba, alpha):
    out = np.zeros((*mask.shape, 4), dtype=np.float32)
    out[mask] = (rgba[0], rgba[1], rgba[2], alpha)
    return out


def rgba_from_binary_mask_thresholded(image, mask, label, hu_lo, hu_hi, alpha):
    mask = (mask == label)
    red = mask & (image >= hu_lo) & (image <= hu_hi)
    yellow = mask & (image < hu_lo)
    # red = mask & (image <= hu_lo) & (image >= hu_hi)
    # yellow = mask & (image > hu_lo) & (image < hu_hi)
    overlay = np.zeros((*image.shape, 4), dtype=np.float32)
    overlay[red] = (1.0, 0.0, 0.0, alpha)
    overlay[yellow] = (1.0, 1.0, 0.0, alpha)
    return overlay


def on_change(value):
    axes[1].clear()
    axes[1].imshow(image, cmap="gray")
    axes[1].imshow(rgba_from_binary_mask_thresholded(image, muscle_mask, label=1, hu_lo=value, hu_hi=hu_hi, alpha=1))
    axes[1].axis("off")
    axes[1].set_title(f"Muscle HU overlay")
    slider_value.set_text(f"Threshold: {value:.1f}")
    fig.canvas.draw_idle()


def main():
    global fig, axes, image, muscle_mask, slider, slider_ax, slider_value

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
    # Left
    axes[0].imshow(image, cmap='gray')
    axes[0].imshow(overlay_muscle)
    axes[0].axis("off")
    axes[0].set_title('Muscle (red)')
    # Right
    axes[1].imshow(image, cmap="gray")
    axes[1].imshow(overlay_myosteatosis)
    axes[1].axis("off")
    axes[1].set_title(f"Muscle low-RA (yellow) and high-RA (red)")
    # Slider
    slider_ax = fig.add_axes([0.15, 0.06, 0.7, 0.03])
    slider = Slider(slider_ax, "Threshold", -29, 150, valinit=hu_lo)
    slider.on_changed(on_change)
    # Slider value text
    slider_value = fig.text(0.5, 0.05, f"Threshold: {hu_lo:.1f}", ha="center", va="center", color='white')
    plt.show()


if __name__ == "__main__":
    main()