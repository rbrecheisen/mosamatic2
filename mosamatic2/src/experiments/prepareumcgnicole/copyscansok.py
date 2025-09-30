import os
import shutil

DATA_DIR_PREP = "D:\\Mosamatic\\NicoleHildebrand\\15-09-2025\\UMCG\\UMCG_scans_NDH_prep"
DATA_DIR_DONE = "D:\\Mosamatic\\NicoleHildebrand\\15-09-2025\\UMCG\\UMCG_scans_NDH_prep_done"
L3_DIR_OK = "D:\\Mosamatic\\NicoleHildebrand\\15-09-2025\\UMCG\\output\\selectslicefromscanstask"

for f in os.listdir(L3_DIR_OK):
    scan_dir_name = os.path.splitext(f)[0]
    scan_dir_name = scan_dir_name[3:]
    source_dir = os.path.join(DATA_DIR_PREP, scan_dir_name)
    if os.path.isdir(source_dir):
        shutil.move(source_dir, DATA_DIR_DONE)
        print(f'Moved scan {scan_dir_name} to {DATA_DIR_DONE}')