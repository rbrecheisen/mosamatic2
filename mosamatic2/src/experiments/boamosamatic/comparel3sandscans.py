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
    "Jeroen Bosch Ziekenhuis (27)",
]

HOSPITAL_NAMES = [
    "Isala Ziekenhuis (21)",
    # "Medisch Spectrum Twente (22)",
    # "MUMC+ (26)",
    # "OLVG Amsterdam (15)",
    # "Radboud UMC (23)",
    # "St. Antonius (13)",
    # "Tjongerschans Heerenveen (19)",
    # "UMC Utrecht (14)",
    # "UMCG (20)": "PORSCH Groningen",
]


def process_file(client, l3_file_path, remote_zip_file_path):
    patient_id = os.path.split(l3_file_path)[1][:-4]
    remote_zip_file_name = os.path.split(remote_zip_file_path)[1]
    local_zip_file_path = os.path.join(constants.LOCAL_ZIP_DIR, remote_zip_file_name)
    local_unzipped_dir_path = None
    local_scan_dir_path = None
    ok = True

    try:
        client.download_sync(remote_path=remote_zip_file_path, local_path=local_zip_file_path)
    except Exception as e:
        print(f'Error downloading from MDR (reomte_path={remote_zip_file_path}, local_path={local_zip_file_path})')
        ok = False

    if ok:
        try:
            with zipfile.ZipFile(local_zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(constants.LOCAL_UNZIPPED_DIR)
            local_unzipped_dir_path = os.path.join(constants.LOCAL_UNZIPPED_DIR, patient_id)
        except Exception as e:
            print(f'Error unzipping downloaded file (local_zip_file_path={local_zip_file_path})')
            ok = False

    if ok:
        try:            
            l3_series_instance_uid = utils.get_series_instance_uid(l3_file_path)
        except Exception as e:
            print(f'Error retrieving SeriesInstanceUID from L3 (l3_file_path={l3_file_path})')
            ok = False

    if ok:
        try:
            for root, dirs, files in os.walk(local_unzipped_dir_path):
                found = False
                for f in files:
                    f_path = os.path.join(root, f)
                    if utils.is_dicom(f_path) and f != 'DICOMDIR':
                        series_instance_uid = utils.get_series_instance_uid(f_path)
                        if series_instance_uid == l3_series_instance_uid:
                            parent_dir_path = utils.get_parent_path(f_path)
                            local_scan_dir_path = os.path.join(constants.LOCAL_SCAN_DIR, patient_id)
                            shutil.copytree(parent_dir_path, local_scan_dir_path, dirs_exist_ok=True)
                            found = True
                            break
                if found:
                    break
        except Exception as e:
            print(f'Error searching or copying CT scan corresponding to L3 (local_unzipped_dir_path={local_unzipped_dir_path})')
            ok = False

    if ok:
        try:            
            local_nifti_file_path = os.path.join(constants.LOCAL_SCAN_NIFTI_DIR, f'{patient_id}.nii.gz')
            dicom2nifti.dicom_series_to_nifti(local_scan_dir_path, local_nifti_file_path)
        except Exception as e:
            print(f'Error converting CT scan to NIFTI (local_scan_dir_path={local_scan_dir_path}, local_nifti_file_path={local_nifti_file_path})')
            ok = False

    try:
        os.remove(local_zip_file_path)
        if local_unzipped_dir_path:
            shutil.rmtree(local_unzipped_dir_path)
        if local_scan_dir_path:
            shutil.rmtree(local_scan_dir_path)
    except Exception as e:
        print(f'Error cleaning up')


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