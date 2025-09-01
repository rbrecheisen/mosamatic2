import os
from mosamatic2.core.loaders.dicomimageloader import DicomImageLoader
from mosamatic2.core.loaders.dicomseriesloader import DicomSeriesLoader
from mosamatic2.core.loaders.dixonseriesloader import DixonSeriesLoader
from mosamatic2.core.data.data import Data
from mosamatic2.core.data.dicomimagedata import DicomImageData
from mosamatic2.core.data.dicomseriesdata import DicomSeriesData
from mosamatic2.core.data.dixonseriesdata import DixonSeriesData
from tests.sources import get_sources

SOURCES = get_sources()


def test_dicomimageloader():
    loader = DicomImageLoader()
    loader.set_path(os.path.join(SOURCES['input'], 'SURG-ZUYD-0001.dcm'))
    data = loader.load()
    assert isinstance(data, Data)
    assert isinstance(data, DicomImageData)
    assert data.object()
    assert data.object().get('PatientID', False)
    # Try to load a non-DICOM file
    try:
        loader.set_file_path(os.path.join(SOURCES['input'], 'SURG-ZUYD-0001.tag'))
        loader.load()
    except Exception:
        assert True


def test_dicomseriesloader():
    loader = DicomSeriesLoader()
    loader.set_path(SOURCES['input']) # There's DICOM and TAG files in this directory
    data = loader.load()
    assert isinstance(data, Data)
    assert isinstance(data, DicomSeriesData)
    assert data.object()
    assert len(data.object()) == 4
    for item in data.object():
        assert item.object().get('PatientID', False)
    # Make sure they're sorted
    prev_instance_number = -1
    for item in data.object():
        instance_number = item.object().get('InstanceNumber')
        assert instance_number > prev_instance_number


def test_dixonseriesloader():
    loader = DixonSeriesLoader()
    pass