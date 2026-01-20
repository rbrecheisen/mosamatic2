import os
import shutil
import zipfile


DATA_DIR = 'M:/data/lauracools/testt4selectiontotalseg/original'
DATA_UNZIPPED_DIR = 'M:/data/lauracools/testt4selectiontotalseg/original_unzipped'
DATA_UNZIPPED_NODOTS_DIR = 'M:/data/lauracools/testt4selectiontotalseg/original_unzipped_nodots'
os.makedirs(DATA_UNZIPPED_DIR, exist_ok=True)
os.makedirs(DATA_UNZIPPED_NODOTS_DIR, exist_ok=True)


for f in os.listdir(DATA_DIR):
    f_path = os.path.join(DATA_DIR, f)
    if f.endswith('.zip'):

        unzipped_dir_path = os.path.join(DATA_UNZIPPED_DIR, f[:-4])
        os.makedirs(unzipped_dir_path, exist_ok=True)
        
        with zipfile.ZipFile(f_path, 'r') as zf:
            zf.extractall(unzipped_dir_path)

            unzipped_nodots_dir_path = os.path.join(DATA_UNZIPPED_NODOTS_DIR, f[:-4])
            os.makedirs(unzipped_nodots_dir_path, exist_ok=True)
            
            for dicom_file in os.listdir(unzipped_dir_path):
                dicom_file_path = os.path.join(unzipped_dir_path, dicom_file)
                if dicom_file.startswith('.'):
                    shutil.copy(dicom_file_path, os.path.join(unzipped_nodots_dir_path, dicom_file[1:]))
                else:
                    shutil.copy(dicom_file_path, unzipped_nodots_dir_path)
            print(f'Extracted {f}')