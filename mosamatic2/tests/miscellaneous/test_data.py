import os
import pydicom
from mosamatic2.core.data.filedata import FileData
from mosamatic2.core.data.dicomimage import DicomImage
from mosamatic2.core.data.dicomimageseries import DicomImageSeries
from mosamatic2.core.data.multidicomimage import MultiDicomImage
from mosamatic2.core.data.dixonseries import DixonSeries
from tests.sources import get_sources

SOURCES = get_sources()


def test_filedata():
    data = FileData()
    data.set_path('/path/to/file')
    assert data.name() == 'file'


def test_dicomimage():
    data = DicomImage()
    data.set_path(os.path.join(SOURCES['input'], 'SURG-ZUYD-0001.dcm'))
    assert data.load()
    assert data.name() == 'SURG-ZUYD-0001.dcm'
    assert isinstance(data.object(), pydicom.FileDataset)


def test_dicomseries():
    data = DicomImageSeries()
    data.set_path(SOURCES['scans'])
    assert data.load()
    assert data.name() == 'CT'
    assert len(data.images()) > 0
    assert isinstance(data.images()[0], DicomImage)
    assert isinstance(data.images()[0].object(), pydicom.FileDataset)
    # Make sure DICOM images are sorted inside this series
    instance_number = -1
    for image in data.images():
        assert image.object().InstanceNumber > instance_number
        instance_number = image.object().InstanceNumber


def test_multidicomimage():
    data = MultiDicomImage()
    data.set_path(SOURCES['input'])
    assert data.load()
    assert data.name() == 'L3'
    assert len(data.images()) > 0
    assert isinstance(data.images()[0], DicomImage)
    assert isinstance(data.images()[0].object(), pydicom.FileDataset)


def test_dixonseries():
    pass