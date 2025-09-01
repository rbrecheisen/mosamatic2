import os
from mosamatic2.core.managers.datamanager import DataManager
from mosamatic2.core.loaders.dicomseriesloader import DicomSeriesLoader
from mosamatic2.core.data.data import Data
from mosamatic2.core.data.dicomimagedata import DicomImageData
from mosamatic2.core.data.dicomseriesdata import DicomSeriesData
from mosamatic2.core.utils import mosamatic_data_dir


def test_datamanager():
    loader = DicomSeriesLoader()
    loader.set_path('D:\\Mosamatic\\MaximeDewulf\\CT_PVP')
    data = loader.load()
    assert isinstance(data, Data)
    assert isinstance(data, DicomSeriesData)
    assert data.object()
    for item in data.object():
        assert isinstance(item, DicomImageData)
    data_manager = DataManager()
    data_manager.add(data)
    assert len(data_manager.print(suppress_output=True)) == 1
    data_manager.save_data_to_json()
    assert os.path.isfile(os.path.join(mosamatic_data_dir(), 'data.json'))
    data_manager.remove_all()
    assert len(data_manager.print(suppress_output=True)) == 0
    data_manager.load_data_from_json()
    assert len(data_manager.print(suppress_output=True)) == 1