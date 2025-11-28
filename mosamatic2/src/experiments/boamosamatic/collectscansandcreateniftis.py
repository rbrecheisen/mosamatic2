import os
import shutil
import zipfile
import utils
import constants
import dicom2nifti

DONE = [
    "Amphia Ziekenhuis (18)",
    "AUMC", # (11)
    "Catharina Ziekenhuis (24)",
    "Erasmus MC (17)",
    "LUMC (28)",
    "Isala Ziekenhuis (21)",
    "Jeroen Bosch Ziekenhuis (27)",
    "Medisch Spectrum Twente (22)",
    "MUMC+ (26)", # ERROR (could not find CT scan corresponding to L3)
    "OLVG Amsterdam (15)",
    "Radboud UMC (23)",
    "St. Antonius (13)", # ERROR (could not find CT scan corresponding to L3)
    "Tjongerschans Heerenveen (19)",
    "UMC Utrecht (14)",
    "UMCG (20)",
]

HOSPITAL_NAMES = [
]


def download_zip_file(client, remote_zip_file_path, local_zip_file_path):
    print(f'Downloading {remote_zip_file_path}...')
    client.download_sync(remote_path=remote_zip_file_path, local_path=local_zip_file_path)
    return local_zip_file_path


def unpack_zip_file(local_zip_file_path, local_unzipped_dir, patient_id):
    print(f'Unpacking {local_zip_file_path} to {local_unzipped_dir}...')
    with zipfile.ZipFile(local_zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(local_unzipped_dir)
    local_unzipped_dir_path = os.path.join(local_unzipped_dir, patient_id)
    return local_unzipped_dir_path


def get_series_instance_uid(file_path):
    series_instance_uid = utils.get_series_instance_uid(file_path)
    return series_instance_uid


def find_scan_with_series_instance_uid(local_unzipped_dir_path, l3_series_instance_uid, patient_id):
    print(f'Finding CT scan in {local_unzipped_dir_path} with SUID = {l3_series_instance_uid}...')
    local_scan_dir_path = None
    found = False
    for root, dirs, files in os.walk(local_unzipped_dir_path):
        for f in files:
            f_path = os.path.join(root, f)
            if utils.is_valid_dicom(f_path):
                series_instance_uid = utils.get_series_instance_uid(f_path)
                if series_instance_uid == l3_series_instance_uid:
                    parent_dir_path = utils.get_parent_path(f_path)
                    local_scan_dir_path = os.path.join(constants.LOCAL_SCAN_DIR, patient_id)
                    shutil.copytree(parent_dir_path, local_scan_dir_path, dirs_exist_ok=True)
                    print(f'Found CT scan')
                    found = True
                    break
        if found:
            break
    return local_scan_dir_path


def convert_scan_to_nifti(local_scan_dir_path, local_scan_nifti_dir, patient_id):
    print(f'Converting CT scan to NIFTI...')
    local_nifti_file_path = os.path.join(local_scan_nifti_dir, f'{patient_id}.nii.gz')
    dicom2nifti.dicom_series_to_nifti(local_scan_dir_path, local_nifti_file_path)
    return local_nifti_file_path


def delete_temp_dirs(local_zip_file_path, local_unzipped_dir_path, local_scan_dir_path):
    print(f'Deleting temporary directories...')
    try:
        os.remove(local_zip_file_path)
        if local_unzipped_dir_path:
            shutil.rmtree(local_unzipped_dir_path)
        if local_scan_dir_path:
            shutil.rmtree(local_scan_dir_path)
    except Exception as e:
        print(f'Error cleaning up')


def process_file(client, l3_file_path, remote_zip_file_path):
    patient_id = os.path.split(l3_file_path)[1][:-4]
    remote_zip_file_name = os.path.split(remote_zip_file_path)[1]
    local_zip_file_path = os.path.join(constants.LOCAL_ZIP_DIR, remote_zip_file_name)
    local_unzipped_dir_path = None
    local_scan_dir_path = None

    try:
        local_zip_file_path = download_zip_file(client, remote_zip_file_path, local_zip_file_path)
        local_unzipped_dir_path = unpack_zip_file(local_zip_file_path, constants.LOCAL_UNZIPPED_DIR, patient_id)
        l3_series_instance_uid = get_series_instance_uid(l3_file_path)
        if l3_series_instance_uid:
            local_scan_dir_path = find_scan_with_series_instance_uid(local_unzipped_dir_path, l3_series_instance_uid, patient_id)
            if local_scan_dir_path:
                convert_scan_to_nifti(local_scan_dir_path, constants.LOCAL_SCAN_NIFTI_DIR, patient_id)
            else:
                print(f'Could not find CT scan in unpacked ZIP file directory')
        else:
            print(f'Could not find SeriesInstanceUID in L3 file path: {l3_file_path}')
    except Exception as e:
        print(f'Error occurred ({e}). Skipping...')
    finally:
        delete_temp_dirs(local_zip_file_path, local_unzipped_dir_path, local_scan_dir_path)


def count_nr_scans_to_process(file_mapping):
    count = 0
    for l3_file_path, _ in file_mapping.items():
        hospital_name = utils.get_parent_name(l3_file_path)
        if hospital_name in HOSPITAL_NAMES:
            count += 1
    return count


def main():
    client = utils.get_webdav_client()
    file_mapping = utils.load_dictionary('filemapping.json')
    start_time = utils.current_time_in_seconds()

    count = count_nr_scans_to_process(file_mapping)
    print(f'Found {count} scans to process')

    for l3_file_path, remote_zip_file_path in file_mapping.items():
        local_hospital_name = utils.get_parent_name(l3_file_path)

        if local_hospital_name in HOSPITAL_NAMES:
            start_time_inner = utils.current_time_in_seconds()
            print(f'Processing {l3_file_path}...')
            process_file(client, l3_file_path, remote_zip_file_path)
            elapsed_time_inner = utils.elapsed_time_in_seconds(start_time_inner)
            print(f'Elapsed time: {utils.duration(elapsed_time_inner)}')

    elapsed_time = utils.elapsed_time_in_seconds(start_time)
    print(f'Total elapsed time: {utils.duration(elapsed_time)}')


if __name__ == '__main__':
    main()