import os
import shutil
from mosamatic2.core import utils


def main():
    source_dir = '/Users/ralph/Desktop/downloads/coco/Archief'
    target_dir = '/Users/ralph/Desktop/downloads/coco/Archief_prep'
    os.makedirs(target_dir, exist_ok=True)
    for root, dirs, files in os.walk(source_dir):
        for f in files:
            f_path = os.path.join(root, f)
            if os.path.isfile(f_path) and utils.is_dicom(f_path) and not f == 'DICOMDIR':
                shutil.copyfile(f_path, os.path.join(target_dir, f + '.dcm'))
                print(f_path)


if __name__ == '__main__':
    main()