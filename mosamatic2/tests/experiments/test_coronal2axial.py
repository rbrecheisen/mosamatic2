import os
import pytest
import shutil
import numpy as np
import SimpleITK as sitk
import matplotlib.pyplot as plt
from mosamatic2.core.utils import load_dicom

DICOM_DIR = 'D:\\Mosamatic\\NicoleHildebrand\\24-06-2025_coronale_CT\\MUMC004_3_coronaal'
DICOM_DIR_RENAMED = 'D:\\Mosamatic\\NicoleHildebrand\\24-06-2025_coronale_CT\\MUMC004_3_coronaal_renamed'
DICOM_DIR_DECOMPRESSED = 'D:\\Mosamatic\\NicoleHildebrand\\24-06-2025_coronale_CT\\MUMC004_3_coronaal_decompressed'
NIFTI_OUTPUT_FILE = 'D:\\Mosamatic\\NicoleHildebrand\\24-06-2025_coronale_CT\\MUMC004_3_coronaal.nii.gz'


def load_dicom_series():
    os.makedirs(DICOM_DIR_RENAMED, exist_ok=True)
    os.makedirs(DICOM_DIR_DECOMPRESSED, exist_ok=True)
    for f in os.listdir(DICOM_DIR):
        f_path = os.path.join(DICOM_DIR, f)
        shutil.copyfile(f_path, os.path.join(DICOM_DIR_RENAMED, f[1:]))
    for f in os.listdir(DICOM_DIR_RENAMED):
        f_path = os.path.join(DICOM_DIR_RENAMED, f)
        p = load_dicom(f_path)
        p.decompress()
        p.save_as(os.path.join(DICOM_DIR_DECOMPRESSED, f))
    reader = sitk.ImageSeriesReader()
    series_IDs = reader.GetGDCMSeriesIDs(DICOM_DIR_DECOMPRESSED)
    if not series_IDs:
        raise RuntimeError(f"No DICOM series found in {DICOM_DIR_DECOMPRESSED}")
    series_file_names = reader.GetGDCMSeriesFileNames(DICOM_DIR_DECOMPRESSED, series_IDs[0])
    reader.SetFileNames(series_file_names)
    img = reader.Execute()
    return img


def resample_isotropic(img, new_spacing=(1.0, 1.0, 1.0)):
    orig_spacing = img.GetSpacing()
    orig_size = img.GetSize()
    new_size = [
        int(round(orig_size[i] * (orig_spacing[i] / new_spacing[i])))
        for i in range(3)
    ]
    resampled = sitk.Resample(
        img,
        new_size,
        sitk.Transform(),
        sitk.sitkLinear,
        img.GetOrigin(),
        new_spacing,
        img.GetDirection(),
        0,
        img.GetPixelID()
    )
    return resampled


def reformat_coronal_to_axial(img):
    arr = sitk.GetArrayFromImage(img)   # shape: (z, y, x)
    axial_arr = np.transpose(arr, (1, 0, 2))  # (z,y,x) -> (y,z,x)
    axial_img = sitk.GetImageFromArray(axial_arr)
    axial_img.SetSpacing(img.GetSpacing())  # keep spacing isotropic
    return axial_img


def preview_slices(img, num_slices=6):
    arr = sitk.GetArrayFromImage(img)  # z,y,x
    z_slices = arr.shape[0]
    step = max(1, z_slices // num_slices)
    indices = list(range(0, z_slices, step))[:num_slices]
    fig, axes = plt.subplots(1, len(indices), figsize=(15, 5))
    for ax, idx in zip(axes, indices):
        ax.imshow(arr[idx, :, :], cmap="gray", vmin=-200, vmax=300)
        ax.set_title(f"Slice {idx}")
        ax.axis("off")
    plt.tight_layout()
    plt.show()


@pytest.mark.filterwarnings('ignore::UserWarning')
@pytest.mark.filterwarnings('ignore::DeprecationWarning')
def test_coronal2axial():
    img = load_dicom_series()
    resampled = resample_isotropic(img, new_spacing=(1.0, 1.0, 1.0))
    axial = reformat_coronal_to_axial(resampled)
    sitk.WriteImage(axial, NIFTI_OUTPUT_FILE)
    preview_slices(axial, num_slices=6)