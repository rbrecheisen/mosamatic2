import os
from mosamatic2.core.tasks import SelectSliceFromScansTask


def test_selectslicefromscans():
    task = SelectSliceFromScansTask(
        inputs={'scans': 'M:\\data\\mosamatic\\test\\CT\\abdomen'},
        params={'vertebra': 'L3'},
        output='M:\\data\\mosamatic\\test\\output',
        overwrite=True,
    )
    task.run()
    output_dir = os.path.join(task.output())
    assert os.path.exists(output_dir), 'Output directory does not exist'
    assert os.path.isfile(os.path.join(output_dir, 'L3_patient1.dcm'))