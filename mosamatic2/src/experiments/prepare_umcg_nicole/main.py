import os
import shutil
import pydicom

DATA_DIR = "D:\\Mosamatic\\NicoleHildebrand\\15-09-2025\\UMCG_scans_NDH"
DATA_DIR_PREP = "D:\\Mosamatic\\NicoleHildebrand\\15-09-2025\\UMCG_scans_NDH_prep"


def is_dicom(f_path):
    try:
        pydicom.dcmread(f_path, stop_before_pixels=True)
        return True
    except:
        return False


for d in os.listdir(DATA_DIR):
    if d.startswith('HPB_'):
        source_dir = os.path.join(DATA_DIR, d)
        target_dir = os.path.join(DATA_DIR_PREP, d)
        os.makedirs(target_dir, exist_ok=True)
        for root, dirs, files in os.walk(source_dir):
            for f in files:
                source = os.path.join(root, f)
                if is_dicom(source):
                    shutil.copy(source, target_dir)
                    print(f'copied {source} to {target_dir}')