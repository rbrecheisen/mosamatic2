import os

from mosamatic2.core.tasks import SelectSliceFromScansTask
from tests.sources import get_sources

SOURCES = get_sources()


def test_selectslicefromscans():
    task = SelectSliceFromScansTask(
        inputs={'scans': SOURCES['scans']},
        params={'vertebra': 'L3'},
        output=SOURCES['output'],
        overwrite=True,
    )
    task.run()
    output_dir = os.path.join(SOURCES['output'], 'selectslicefromscanstask')
    assert os.path.exists(output_dir), 'Output directory does not exist'
    assert os.path.isfile(os.path.join(output_dir, 'L3_patient1.dcm'))