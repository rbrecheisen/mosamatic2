import os
import shutil
import constants


def find_l3_for_nifti_file(nifti_base_file_name):
    for root, dirs, files in os.walk(constants.LOCAL_L3_DIR):
        for f in files:
            if f == nifti_base_file_name + '.dcm':
                return os.path.join(root, f)
    return None


def main():
    for nifti_file_name in os.listdir(constants.LOCAL_SCAN_NIFTI_DIR):
        nifti_base_file_name = nifti_file_name[:-7]
        l3_file_path = find_l3_for_nifti_file(nifti_base_file_name)
        if l3_file_path:
            shutil.copy(l3_file_path, constants.LOCAL_SCAN_NIFTI_L3_DIR)


if __name__ == '__main__':
    main()