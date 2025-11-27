import os
import time
import math
import json
import pydicom
import pydicom.errors
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


def load_dictionary(file_name, reverse=False):
    dictionary = None
    with open(get_path(file_name), 'r') as f:
        dictionary = json.load(f)
    if reverse:
        return {v: k for k, v in dictionary.items()}
    return dictionary


def save_dictionary(dictionary, file_name):
    with open(get_path(file_name), 'w') as f:
        json.dump(dictionary, f, indent=4)


def is_number(value):
    try:
        int(value)
        return True
    except:
        return False
    

def is_valid_dicom(f_path):
    try:
        p = pydicom.dcmread(f_path, stop_before_pixels=True)
        if 'Modality' in p and p.Modality == 'CT' and 'SeriesInstanceUID' in p:
            return True
        return False
    except pydicom.errors.InvalidDicomError:
        return False
    

def get_series_instance_uid(file_path):
    p = pydicom.dcmread(file_path, stop_before_pixels=True)
    return p.SeriesInstanceUID


def current_time_in_milliseconds():
    return int(round(time.time() * 1000))


def current_time_in_seconds() -> int:
    return int(round(current_time_in_milliseconds() / 1000.0))


def elapsed_time_in_milliseconds(start_time_in_milliseconds):
    return current_time_in_milliseconds() - start_time_in_milliseconds


def elapsed_time_in_seconds(start_time_in_seconds):
    return current_time_in_seconds() - start_time_in_seconds


def duration(seconds):
    h = int(math.floor(seconds/3600.0))
    remainder = seconds - h * 3600
    m = int(math.floor(remainder/60.0))
    remainder = remainder - m * 60
    s = int(math.floor(remainder))
    return '{} hours, {} minutes, {} seconds'.format(h, m, s)