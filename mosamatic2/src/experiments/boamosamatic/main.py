import os
import constants
from utils import (
    print_dictionary, 
    load_dictionary, 
    save_dictionary, 
    get_path, 
    get_parent_path,
    get_parent_name,
    is_number,
    get_webdav_client,
)

client = get_webdav_client()


def load_image_file_paths():
    image_file_paths = []
    for d in os.listdir(constants.LOCAL_L3_BASE_DIR):
        d_path = os.path.join(constants.LOCAL_L3_BASE_DIR, d)
        if os.path.isdir(d_path):
            for f in os.listdir(d_path):
                if is_number(f):
                    image_file_paths.append(os.path.join(d_path, f))
    return image_file_paths


def main():
    folder_mapping = load_dictionary('folder_mapping.json')
    image_file_paths = load_image_file_paths()


if __name__ == '__main__':
    main()


# def create_folder_l3_image_mapping(folder_mapping):
#     l3_image_mapping = {}
#     for local_folder_name, remote_folder_name in folder_mapping.items():
#         local_folder_path = os.path.join(constants.LOCAL_L3_BASE_DIR, local_folder_name)
#         l3_image_mapping[local_folder_name] = []
#         for file_name in os.listdir(local_folder_path):
#             if is_number(file_name):
#                 file_path = os.path.join(local_folder_path, file_name)
#                 l3_image_mapping[local_folder_name].append(file_path)
#     save_dictionary(l3_image_mapping, 'folder_l3_image_mapping.json')
#     return l3_image_mapping


# def download_zip_file_from_remote(file_name, remote_folder_name):
#     remote_folder_path = f'{constants.MDR_PROJECT_ID}/{constants.MDR_COLLECTION_ID}/{remote_folder_name}'
#     file_name_no_ext = file_name.split('.')[0]
#     zip_file_name = f'{file_name_no_ext}.zip'
#     zip_file_path = f'{remote_folder_path}/{zip_file_name}'
#     if CLIENT.check(zip_file_path):
#         print(f'ZIP file found')
#     return ''


# def create_l3_to_scan_mapping(folder_mapping):
#     l3_to_remote_scan_mapping = {}
#     for local_folder_name, remote_folder_name in folder_mapping.items():
#         local_folder_path = os.path.join(constants.LOCAL_L3_BASE_DIR, local_folder_name)
#         l3_to_remote_scan_mapping[local_folder_name] = {}
#         for file_name in os.listdir(local_folder_path):
#             if is_number(file_name):
#                 file_path = os.path.join(local_folder_path, file_name)
#                 zip_file_path = download_zip_file_from_remote(file_name, remote_folder_name)

#             l3_to_remote_scan_mapping[local_folder_name][file_path] = ''
#         # print_dictionary(l3_to_remote_scan_mapping[local_folder_name])
#     return l3_to_remote_scan_mapping
