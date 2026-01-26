import os
import shutil
import pydicom
import pydicom.errors


DATA_DIR = 'M:\\data\\contrastsensitivity\\lieke\\original'
DATA_DIR_PREPARED = 'M:\\data\\contrastsensitivity\\lieke\\orirginal_prepared'
PHASES = [
    'unenhanced', 
    'arterial', 
    'venous',
]


def print_phases(d_path):
    phases = []
    for d in os.listdir(d_path):
        phases.append(d)
    print(', '.join(phases))


def is_dicom(f_path):
    try:
        pydicom.dcmread(f_path, stop_before_pixels=True)
        return True
    except pydicom.errors.InvalidDicomError:
        return False


def get_file(d_path):
    for root, dirs, files in os.walk(d_path):
        for f in files:
            if f != 'DICOMDIR':
                f_path = os.path.join(root, f)
                if is_dicom(f_path):
                    return f_path
    return None


def main():
    for d in os.listdir(DATA_DIR):
        d_path = os.path.join(DATA_DIR, d)
        if os.path.isdir(d_path):
            for phase_dir in os.listdir(d_path):
                if phase_dir in PHASES:
                    phase_dir_path = os.path.join(d_path, phase_dir)
                    if os.path.isdir(phase_dir_path):
                        f_path = get_file(phase_dir_path)
                        if f_path:
                            f_name = f'{d}_{phase_dir}.dcm'
                            shutil.copy(f_path, os.path.join(DATA_DIR_PREPARED, f_name))


if __name__ == '__main__':
    main()