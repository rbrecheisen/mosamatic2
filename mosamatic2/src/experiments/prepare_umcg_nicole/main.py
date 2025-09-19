import os
import shutil
from mosamatic2.core.utils import is_dicom, load_dicom

DATA_DIR = "D:\\Mosamatic\\NicoleHildebrand\\15-09-2025\\UMCG_scans_NDH"
DATA_DIR_PREP = "D:\\Mosamatic\\NicoleHildebrand\\15-09-2025\\UMCG_scans_NDH_prep"


for d in os.listdir(DATA_DIR):
    if d.startswith('HPB_'):
        print(f'Processing {d}...')
        source_dir = os.path.join(DATA_DIR, d) # e.g. HPB_1
        # Find one or more series per patients
        series_list = {}
        for root, dirs, files in os.walk(source_dir):
            for f in files:
                f_path = os.path.join(root, f)
                if is_dicom(f_path):
                    p = load_dicom(f_path, stop_before_pixels=True)
                    if p:
                        if 'SeriesInstanceUID' in p:
                            if p.SeriesInstanceUID not in series_list.keys():
                                series_list[p.SeriesInstanceUID] = []
                            series_list[p.SeriesInstanceUID].append(f_path)
                        else:
                            print(f'Missing SeriesInstanceUID in DICOM {f_path}')
                    else:
                        print(f'Could not load DICOM {f_path} or missing SeriesInstanceUID')
        # Copy each series to its own target directory
        count = 1
        for k, v in series_list.items():
            target_dir = os.path.join(DATA_DIR_PREP, f'{d}_{count}')
            os.makedirs(target_dir, exist_ok=True)
            for f in v:
                shutil.copy(f, target_dir)
                print(f)
            count += 1