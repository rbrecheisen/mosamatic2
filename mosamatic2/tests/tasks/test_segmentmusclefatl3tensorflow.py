import os
from mosamatic2.core.tasks.segmentmusclefatl3tensorflowtask.segmentmusclefatl3tensorflowtask import SegmentMuscleFatL3TensorFlowTask
from tests.sources import get_sources

SOURCES = get_sources()
TASK_NAME = 'SegmentMuscleFatL3TensorFlowTask'.lower()


def test_segmentmusclefatl3tensorflow():
    task = SegmentMuscleFatL3TensorFlowTask(
        inputs={
            'images': 'D:\\Mosamatic\\TestData\\L3',
            'model_files': 'D:\\Mosamatic\\TensorFlowModelFiles',
        }, 
        params={'model_version': 1.0},
        output='D:\\Mosamatic\\TestData\\output',
        overwrite=True,
    )
    task.run()
    for f in os.listdir(task.input('images')):
        if f.endswith('.dcm'):
            target_name = f[:-4] + '.dcm.seg.npy'
            assert os.path.isfile(os.path.join(task.output(), target_name))