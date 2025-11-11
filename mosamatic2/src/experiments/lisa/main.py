import os
import shutil
import zipfile


DATA_DIR = 'E:\\'
OUTPUT_DIR = 'D:\\Mosamatic\\Lisa'
RENAMED_DIR = 'D:\\Mosamatic\\Lisa\\Renamed'
os.makedirs(RENAMED_DIR, exist_ok=True)


for f in os.listdir(DATA_DIR):
    if f.startswith('L3_MUMC') and f.endswith('.zip'):
        f_path = os.path.join(DATA_DIR, f)
        with zipfile.ZipFile(f_path) as zip_ref:
            output_dir = os.path.join(OUTPUT_DIR, f)
            zip_ref.extractall(output_dir)
            dicom_file = os.listdir(output_dir)[0]
            dicom_file_path = os.path.join(output_dir, dicom_file)
            new_dicom_file = f + '.dcm'
            new_dicom_file_path = os.path.join(RENAMED_DIR, new_dicom_file)
            shutil.copyfile(dicom_file_path, new_dicom_file_path)
            print(new_dicom_file_path)