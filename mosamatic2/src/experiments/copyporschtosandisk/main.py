import os
import shutil
import zipfile
import utils


LOCAL_ZIP_DIR = 'M:\\data\\porsch\\original\\zip'
HOSPITALS = [
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


def download_zip_file(client, remote_zip_file_path, hospital_name):
    remote_zip_file_name = os.path.split(remote_zip_file_path)[1]
    local_hospital_path = os.path.join(LOCAL_ZIP_DIR, hospital_name)
    os.makedirs(local_hospital_path, exist_ok=True)
    local_zip_file_path = os.path.join(local_hospital_path, remote_zip_file_name)
    print(f'Downloading {remote_zip_file_path} to {local_zip_file_path}...')
    client.download_sync(remote_path=remote_zip_file_path, local_path=local_zip_file_path)
    return local_zip_file_path


def count_nr_scans_to_process(file_mapping):
    count = 0
    for l3_file_path, _ in file_mapping.items():
        hospital_name = utils.get_parent_name(l3_file_path)
        if hospital_name in HOSPITALS:
            count += 1
    return count


def main():
    client = utils.get_webdav_client()
    file_mapping = utils.load_dictionary('filemapping.json')
    print(f'Found {count_nr_scans_to_process(file_mapping)} scans to process')
    start_time = utils.current_time_in_seconds()
    for l3_file_path, remote_zip_file_path in file_mapping.items():
        local_hospital_name = utils.get_parent_name(l3_file_path)
        if local_hospital_name in HOSPITALS:
            start_time_inner = utils.current_time_in_seconds()
            download_zip_file(client, remote_zip_file_path, local_hospital_name)
            print(f'Elapsed time: {utils.duration(utils.elapsed_time_in_seconds(start_time_inner))}')
    print(f'Total elapsed time: {utils.duration(utils.elapsed_time_in_seconds(start_time))}')


if __name__ == '__main__':
    main()