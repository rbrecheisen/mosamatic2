import os
import shutil


DATA_DIR = 'M:/data/lauracools/testt4selectiontotalseg/original_unzipped\STS001_CT-thorax'
DATA_OUTPUT_DIR = 'M:/data/lauracools/testt4selectiontotalseg/original_unzipped_nodots\STS001_CT-thorax'
os.makedirs(DATA_OUTPUT_DIR, exist_ok=True)

for f in os.listdir(DATA_DIR):
    f_path = os.path.join(DATA_DIR, f)
    if f.startswith('.'):
        shutil.copy(f_path, os.path.join(DATA_OUTPUT_DIR, f[1:]))
    else:
        shutil.copy(f_path, DATA_OUTPUT_DIR)
    print(f_path)