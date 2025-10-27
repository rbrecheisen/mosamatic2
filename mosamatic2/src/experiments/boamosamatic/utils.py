import os
import json
import constants
from pathlib import Path
from webdav3.client import Client


def get_webdav_token():
    token_file_path = 'C:\\Users\\r.brecheisen\\mdr-webdav.txt'
    with open(token_file_path, 'r') as f:
        token = f.readline().strip()
    return token


def get_webdav_client():
    options = {
        'webdav_hostname': "https://download.datahubmaastricht.nl",
        'webdav_login':    "rbrecheise",
        'webdav_password': get_webdav_token(),
    }
    client = Client(options)
    return client


def get_path(file_name):
    return os.path.join(constants.BASE_DIR, file_name)


def get_parent_path(file_path):
    parent = Path(file_path).parent
    return str(parent)


def get_parent_name(file_path):
    return Path(file_path).parent.name


def print_dictionary(dictionary):
    for k, v in dictionary.items():
        print(f'{k}: {v}')


def load_dictionary(file_name):
    with open(get_path(file_name), 'r') as f:
        return json.load(f)


def save_dictionary(dictionary, file_name):
    with open(get_path(file_name), 'w') as f:
        json.dump(dictionary, f, indent=4)


def is_number(file_name):
    try:
        patient_nr = file_name.split('.')[0]
        int(patient_nr)
        return True
    except:
        return False