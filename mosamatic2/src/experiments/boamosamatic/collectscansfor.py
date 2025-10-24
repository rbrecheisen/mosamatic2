import os
import json
import argparse
from experiments.boamosamatic.webdav import get_webdav_client

BASE_DIR = 'D:\\SoftwareDevelopment\\GitHub\\mosamatic2\\mosamatic2\\src\\experiments\\boamosamatic'

MDR_PROJECT_ID = 'P000000420'       # PORSCH trial
MDR_COLLECTION_ID = 'C000000002'    # PORSCH trial CT scans

LOCAL_L3_BASE_DIR = 'L:\\FHML_SURGERY\\Mosamatic\\Projects\\P0009_PORSCH (Nicole Hildebrand)\\L3'
LOCAL_ZIP_FILES_BASE_DIR = 'D:\\Mosamatic\\NicoleHildebrand\\PORSCH\\ZIPS'
LOCAL_SCANS_BASE_DIR = 'D:\\Mosamatic\\NicoleHildebrand\\PORSCH\\SCANS'


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('local_folder', help='Collect CT scans for local folder')
    args = parser.parse_args()
    return args


def download_zip_file_for(l3_file_path):
    pass


def unpack_zip_file(zip_file_path):
    pass


def collect_scans_for(local_folder):
    local_folder_path = os.path.join(LOCAL_L3_BASE_DIR, local_folder)
    for l3_file in os.listdir(local_folder_path):
        l3_file_path = os.path.join(local_folder_path, l3_file)
        zip_file_path = download_zip_file_for(l3_file_path)


def main():
    # For each L3 file (with patient number) download corresponding ZIP file
    # Unpack ZIP file
    # Search for CT scan with same SeriesInstanceUID as L3 file
    # Copy CT scan to local SCANS_DIR location

    # args = get_args()
    # collect_scans_for(args.local_folder)

    with open(os.path.join(BASE_DIR, 'folders.json')) as f:
        folder_lookup = json.load(f)
    for local_folder, remote_folder in folder_lookup.items():
        collect_scans_for(local_folder)


if __name__ == '__main__':
    main()