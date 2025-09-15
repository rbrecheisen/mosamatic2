import os
import pydicom
from collections import defaultdict, Counter

ROOT_DIR = 'D:\\Mosamatic\\Dixon\\AllFiles'


def scan_dicom_directory(root_dir):
    results = defaultdict(lambda: defaultdict(Counter))
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                ds = pydicom.dcmread(filepath, stop_before_pixels=True, force=True)
                modality = getattr(ds, "Modality", "UNKNOWN")
                series_desc = getattr(ds, "SeriesDescription", "NoDescription")
                image_type = tuple(getattr(ds, "ImageType", []))
                if modality == "MR":
                    if ("DIXON" in series_desc.upper()) or any(
                        word in str(image_type).upper()
                        for word in ["DIXON", "WATER", "FAT", "IN_PHASE", "OPPOSED_PHASE"]
                    ):
                        modality = "DIXON"
                results[modality][series_desc][image_type] += 1
            except Exception:
                continue
    return results


def test_dicomdir_scan():
    dicom_summary = scan_dicom_directory(ROOT_DIR)
    print("\nDICOM summary:")
    for modality, series_dict in dicom_summary.items():
        print(f"\nModality: {modality}")
        total_modality_files = sum(sum(counter.values()) for counter in series_dict.values())
        print(f"  -> Total files: {total_modality_files}")
        for series, counter in series_dict.items():
            print(f"  Series: {series}")
            for img_type, count in counter.items():
                print(f"    ImageType: {img_type} -> {count} files")