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
