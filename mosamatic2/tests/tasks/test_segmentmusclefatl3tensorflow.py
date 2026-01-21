import os
from mosamatic2.core.tasks.segmentmusclefatl3tensorflowtask.segmentmusclefatl3tensorflowtask import SegmentMuscleFatL3TensorFlowTask


def test_segmentmusclefatl3tensorflow():
    task = SegmentMuscleFatL3TensorFlowTask(
        inputs={
            'images': 'M:\\data\\mosamatic\\test\\L3',
            'model_files': 'M:\\models\\L3\\tensorflow\\1.0',
        }, 
        params={
            'model_version': 1.0,
            'probabilities': False,
        },
        output='M:\\data\\mosamatic\\test\\output',
        overwrite=True,
    )
    task.run()
    for f in os.listdir(task.input('images')):
        if f.endswith('.dcm'):
            target_name = f[:-4] + '.dcm.seg.npy'
            assert os.path.isfile(os.path.join(task.output(), target_name))