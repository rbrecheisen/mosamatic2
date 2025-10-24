import os
import json
import zipfile
import pydicom
from webdav3.client import Client


PROJECT_ID = 'P000000420'    # PORSCH trial
COLLECTION_ID = 'C000000002' # PORSCH trial CT scans
L3_BASE_DIR = 'L:\\FHML_SURGERY\\Mosamatic\\Projects\\P0009_PORSCH (Nicole Hildebrand)\\L3'
DOWNLOAD_DIR = 'D:\\Mosamatic\\NicoleHildebrand\\PORSCH\\ZIPS'


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
                int(patient_nr)
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


def get_l3s_and_scans():

    folder_name_lookup = get_folder_name_lookup()
    folder_patient_nrs = get_folder_patient_nrs()
    folder_l3s = get_folder_l3s()
    client = get_client()

    l3s_and_scans = {}
    for local_folder, remote_folder in folder_name_lookup.items():
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
                print(f' > Downloading ZIP file')
                local_zip_file_path = os.path.join(DOWNLOAD_DIR, zip_file)
                client.download_sync(zip_file_path, local_zip_file_path)
                
                # Unpack ZIP file
                print(f' > Unpacking')
                with zipfile.ZipFile(local_zip_file_path, 'r') as zip_ref:
                    zip_ref.extractall(DOWNLOAD_DIR)
                
                l3_file = folder_l3s[local_folder][patient_nr]
                l3_series_instance_uid = get_series_instance_uid(l3_file)

                # Search for CT scan corresponding to L3 file
                print(f' > Search CT scan corresponding to L3 file')
                stop_search = False
                for root, dirs, files in os.walk(os.path.join(DOWNLOAD_DIR, patient_nr)):
                    for f in files:
                        f_path = os.path.join(root, f)
                        try:
                            p = pydicom.dcmread(f_path, stop_before_pixels=True)
                            if l3_series_instance_uid == p.SeriesInstanceUID:
                                scan_dir = os.path.split(f_path)[0]
                                l3s_and_scans[l3_file] = scan_dir
                                print(f' > Found')
                                stop_search = True
                                break
                        except:
                            pass
                    if stop_search:
                        break
    return l3s_and_scans


l3s_and_scans = get_l3s_and_scans()
for k, v in l3s_and_scans.items():
    print(f'{k}: {v}')