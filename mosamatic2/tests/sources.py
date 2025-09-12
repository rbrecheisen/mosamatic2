import sys

SOURCES = {
    'mac': {
        'input': '/Users/ralph/Library/CloudStorage/GoogleDrive-ralph.brecheisen@gmail.com/My Drive/data/Mosamatic/testdata/L3',
        'scans': '/Users/ralph/Library/CloudStorage/GoogleDrive-ralph.brecheisen@gmail.com/My Drive/data/Mosamatic/testdata/CT',
        'model_files': {
            'pytorch': '/Users/ralph/Library/CloudStorage/GoogleDrive-ralph.brecheisen@gmail.com/My Drive/data/Mosamatic/models/pytorch/L3/2.2',
            'tensorflow': '/Users/ralph/Library/CloudStorage/GoogleDrive-ralph.brecheisen@gmail.com/My Drive/data/Mosamatic/models/tensorflow/L3/1.0',
        },
        'output': '/Users/ralph/Library/CloudStorage/GoogleDrive-ralph.brecheisen@gmail.com/My Drive/data/Mosamatic/testdata/output',
    },
    'windows': {
        'input': 'G:\\My Drive\\data\\Mosamatic\\testdata\\L3',
        'scans': 'G:\\My Drive\\data\\Mosamatic\\testdata\\CT',
        'model_files': {
            'pytorch': 'G:\\My Drive\\data\\Mosamatic\\models\\pytorch\\L3\\2.2',
            'tensorflow': 'G:\\My Drive\\data\\Mosamatic\\models\\tensorflow\\L3\\1.0',
        },
        'output': 'G:\\My Drive\\data\\Mosamatic\\testdata\\output',
    }
}

def get_sources():
    if sys.platform.startswith('darwin'):
        return SOURCES['mac']
    else:
        return SOURCES['windows']