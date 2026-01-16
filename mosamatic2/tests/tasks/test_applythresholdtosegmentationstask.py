import os
from mosamatic2.core.tasks.applythresholdtosegmentationstask.applythresholdtosegmentationstask import ApplyThresholdToSegmentationsTask


def test_applythresholdtosegmentations():
    task = ApplyThresholdToSegmentationsTask(
        inputs={
            'images': 'D:\\Mosamatic\\TestData\\output\\rescaledicomimagestask',
            'segmentations': 'D:\\Mosamatic\\TestData\\output\\segmentmusclefatl3tensorflowtask'
        },
        params={
            'label': 1,
            'threshold_low': 5,
            'threshold_high': 150,
        },
        output='D:\\Mosamatic\\TestData\\output',
        overwrite=True,
    )
    task.run()


if __name__ == '__main__':
    test_applythresholdtosegmentations()