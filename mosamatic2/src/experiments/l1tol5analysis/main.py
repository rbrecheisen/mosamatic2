import os
import shutil
import pydicom
import pydicom.errors
import pandas as pd

ORIGINAL_DIR = "D:\\Mosamatic\\L1-L5\\Original"
ORIGINAL_COLLECTED_DIR = "D:\\Mosamatic\\L1-L5\\OriginalCollected"
SCORES_FILE_PATH = "D:\\Mosamatic\\L1-L5\\Out\\defaultpipeline\\calculatescorestask\\bc_scores.csv"


def is_dicom(f_path):
    try:
        pydicom.dcmread(f_path, stop_before_pixels=True)
        return True
    except pydicom.errors.InvalidDicomError:
        return False
    

def collect_files():
    for d in os.listdir(ORIGINAL_DIR):
        if d.startswith('Patient '):
            d_path = os.path.join(ORIGINAL_DIR, d)
            for f in os.listdir(d_path):
                f_path = os.path.join(d_path, f)
                if os.path.isfile(f_path):
                    if is_dicom(f_path):
                        f_name = os.path.split(f_path)[1]
                        d_name = d.replace(' ', '_')
                        target_f_name = f'{d_name}_{f_name}'
                        target_f_path = os.path.join(ORIGINAL_COLLECTED_DIR, target_f_name)
                        shutil.copy(f_path, target_f_path)
                        print(target_f_path)


def main():
    collect_files()


if __name__ == '__main__':
    main()