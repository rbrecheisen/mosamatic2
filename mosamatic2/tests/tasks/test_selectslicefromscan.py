import os

from mosamatic2.core.tasks import SelectSliceFromScansTask
from tests.sources import get_sources

SOURCES = get_sources()


def test_selectslicefromscans():
    task = SelectSliceFromScansTask(
        inputs={'scans': 'D:\\Mosamatic\\TestData\\CT'},
        params={'vertebra': 'L3'},
        output='D:\\Mosamatic\\TestData\\output',
        overwrite=True,
    )
    task.run()
    output_dir = os.path.join(task.output())
    assert os.path.exists(output_dir), 'Output directory does not exist'
    assert os.path.isfile(os.path.join(output_dir, 'L3_patient1.dcm'))