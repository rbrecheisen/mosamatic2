import os
import shutil
import zipfile
import utils
import constants
import dicom2nifti


def process_file(client, l3_file_path, remote_zip_file_path):
    patient_id = os.path.split(l3_file_path)[1][:-4]
    remote_zip_file_name = os.path.split(remote_zip_file_path)[1]
    local_zip_file_path = os.path.join(constants.LOCAL_ZIP_DIR, remote_zip_file_name)

    client.download_sync(remote_path=remote_zip_file_path, local_path=local_zip_file_path)

    with zipfile.ZipFile(local_zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(constants.LOCAL_UNZIPPED_DIR)
    local_unzipped_dir_path = os.path.join(constants.LOCAL_UNZIPPED_DIR, patient_id)

    local_scan_dir_path = None
    l3_series_instance_uid = utils.get_series_instance_uid(l3_file_path)
    for root, dirs, files in os.walk(local_unzipped_dir_path):
        found = False
        for f in files:
            f_path = os.path.join(root, f)
            series_instance_uid = utils.get_series_instance_uid(f_path)
            if series_instance_uid == l3_series_instance_uid:
                parent_dir_path = utils.get_parent_path(f_path)
                local_scan_dir_path = os.path.join(constants.LOCAL_SCAN_DIR, patient_id)
                shutil.copytree(parent_dir_path, local_scan_dir_path, dirs_exist_ok=True)
                found = True
                break
        if found:
            break

    local_nifti_file_path = os.path.join(constants.LOCAL_SCAN_NIFTI_DIR, f'{patient_id}.nii.gz')
    dicom2nifti.dicom_series_to_nifti(local_scan_dir_path, local_nifti_file_path)

    os.remove(local_zip_file_path)
    shutil.rmtree(local_unzipped_dir_path)
    if local_scan_dir_path:
        shutil.rmtree(local_scan_dir_path)


def main():
    client = utils.get_webdav_client()
    file_mapping = utils.load_dictionary('filemapping.json')
    start_time = utils.current_time_in_seconds()
    hospital_name = 'AUMC'
    for l3_file_path, remote_zip_file_path in file_mapping.items():
        local_hospital_name = utils.get_parent_name(l3_file_path)
        if local_hospital_name == hospital_name:
            start_time_inner = utils.current_time_in_seconds()
            print(f'Processing {l3_file_path}...')
            process_file(client, l3_file_path, remote_zip_file_path)
            elapsed_time_inner = utils.elapsed_time_in_seconds(start_time_inner)
            print(f'Elapsed time: {utils.duration(elapsed_time_inner)}')            
    elapsed_time = utils.elapsed_time_in_seconds(start_time)
    print(f'Total elapsed time: {utils.duration(elapsed_time)}')


if __name__ == '__main__':
    main()