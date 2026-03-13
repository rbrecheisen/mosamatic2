import os
import shutil
import pydicom

DIR_ORG = 'M:\data\impact_emmy_maas\original'
DIR_ORG_FLAT = 'M:\data\impact_emmy_maas\original_flattened'


def main():
    # Check uniques of file names before copying
    files = []
    for f in os.listdir(DIR_ORG):
        if f not in files:
            files.append(f)
        else:
            raise RuntimeError('File already exists!')
    # Copy files to output directory
    for root, dirs, files in os.walk(DIR_ORG):
        for f in files:
            f_path = os.path.join(root, f)
            is_dicom = False
            try:
                pydicom.dcmread(f_path, stop_before_pixels=True)
                is_dicom = True
            except:
                pass
            if is_dicom:
                shutil.copy(f_path, DIR_ORG_FLAT)
                print(f)


if __name__ == '__main__':
    main()