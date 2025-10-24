import os
import json
import zipfile
import shutil
import pydicom
from webdav3.client import Client


PROJECT_ID = 'P000000420'    # PORSCH trial
COLLECTION_ID = 'C000000002' # PORSCH trial CT scans
L3_BASE_DIR = 'L:\\FHML_SURGERY\\Mosamatic\\Projects\\P0009_PORSCH (Nicole Hildebrand)\\L3'
DOWNLOAD_DIR = 'D:\\Mosamatic\\NicoleHildebrand\\PORSCH\\ZIPS'
SCANS_DIR = 'D:\\Mosamatic\\NicoleHildebrand\\PORSCH\\SCANS'


def get_webdav_token():
    token_file_path = 'C:\\Users\\r.brecheisen\\mdr-webdav.txt'
    with open(token_file_path, 'r') as f:
        token = f.readline().strip()
    return token


def get_folder_name_lookup():
    folder_names_file_path = 'folder_names.json'
    with open(folder_names_file_path, 'r') as f:
        folder_name_lookup = json.load(f)
    return folder_name_lookup


def get_folder_patient_nrs():
    folder_name_lookup = get_folder_name_lookup()
    patient_nrs = {}
    for local_folder, value in folder_name_lookup.items():
        patient_nrs[local_folder] = []
        local_folder_path = os.path.join(L3_BASE_DIR, local_folder)
        for f in os.listdir(local_folder_path):
            try:
                patient_nr = f.split('.')[0]
                int(patient_nr) # Only use L3 files with whole numbers as patient ID
                patient_nrs[local_folder].append(patient_nr)
            except:
                pass
    return patient_nrs


def get_folder_l3s():
    folder_name_lookup = get_folder_name_lookup()
    l3s = {}
    for local_folder, value in folder_name_lookup.items():
        l3s[local_folder] = {}
        local_folder_path = os.path.join(L3_BASE_DIR, local_folder)
        for f in os.listdir(local_folder_path):
            try:
                patient_nr = f.split('.')[0]
                int(patient_nr)
                f_path = os.path.join(local_folder_path, f)
                l3s[local_folder][patient_nr] = f_path
            except:
                pass
    return l3s


def get_series_instance_uid(f):
    p = pydicom.dcmread(f, stop_before_pixels=True)
    return p.SeriesInstanceUID


def get_client():
    options = {
        'webdav_hostname': "https://download.datahubmaastricht.nl",
        'webdav_login':    "rbrecheise",
        'webdav_password': get_webdav_token(),
    }
    client = Client(options)
    return client


def get_l3s_and_scans(local_folder):
    folder_name_lookup = get_folder_name_lookup()
    folder_patient_nrs = get_folder_patient_nrs()
    folder_l3s = get_folder_l3s()
    client = get_client()
    l3s_and_scans = {}
    remote_folder = folder_name_lookup[local_folder]
    remote_folder_path = f'{PROJECT_ID}/{COLLECTION_ID}/{remote_folder}'
    patient_nrs = folder_patient_nrs[local_folder]
    # Run through patient numbers
    for patient_nr in patient_nrs:
        print(f'Processing patient {patient_nr}')
        zip_file = f'{patient_nr}.zip'
        zip_file_path = f'{remote_folder_path}/{zip_file}'
        # Check that ZIP file path exists on remote
        if client.check(zip_file_path):
            # Download ZIP file
            local_zip_dir = os.path.join(DOWNLOAD_DIR, local_folder)
            os.makedirs(local_zip_dir, exist_ok=True)
            local_zip_file_path = os.path.join(local_zip_dir, zip_file)
            client.download_sync(zip_file_path, local_zip_file_path)
            # Unpack ZIP file
            with zipfile.ZipFile(local_zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(DOWNLOAD_DIR)
            l3_file = folder_l3s[local_folder][patient_nr]
            l3_series_instance_uid = get_series_instance_uid(l3_file)
            # Search for CT scan corresponding to L3 file
            stop_search = False
            for root, dirs, files in os.walk(os.path.join(local_zip_dir, patient_nr)):
                for f in files:
                    f_path = os.path.join(root, f)
                    try:
                        p = pydicom.dcmread(f_path, stop_before_pixels=True)
                        if l3_series_instance_uid == p.SeriesInstanceUID:
                            scan_dir = os.path.split(f_path)[0]
                            l3s_and_scans[l3_file] = scan_dir
                            stop_search = True
                            break
                    except:
                        pass
                if stop_search:
                    break
    return l3s_and_scans


folder_name_lookup = get_folder_name_lookup()
for local_folder, remote_folder in folder_name_lookup.items():

    # Check if JSON file exists. If so, load mapping from JSON
    json_file = local_folder.replace(' ', '_').lower() + '.json'
    if os.path.isfile(json_file):
        with open(json_file, 'r') as f:
            l3s_and_scans = json.load(f)
    else:
        # # Get mapping from L3 files to scan directories
        # l3s_and_scans = get_l3s_and_scans(local_folder)
        # # Save mapping to JSON
        # with open(json_file, 'w') as f:
        #     json.dump(l3s_and_scans, f)
        pass

    # Copy scan directory files to new directory with L3 file name
    for l3_file, scan_dir in l3s_and_scans.items():
        patient_nr = os.path.split(l3_file)[1].split('.')[0]
        print(f'Copying {scan_dir}')
        os.makedirs(os.path.join(SCANS_DIR, patient_nr), exist_ok=True)
        for f in os.listdir(scan_dir):
            f_path = os.path.join(scan_dir, f)
            shutil.copy(f_path, os.path.join(SCANS_DIR, patient_nr))