from mosamatic2.core.tasks.applythresholdtosegmentationstask.applythresholdtosegmentationstask import ApplyThresholdToSegmentationsTask


def test_applythresholdtosegmentations():
    task = ApplyThresholdToSegmentationsTask(
        inputs={
            'images': 'M:\\data\\mosamatic\\test\\L3',
            'segmentations': 'M:\\data\\mosamatic\\test\\L3',
        },
        params={
            'label': 1,
            'threshold_low': 5,
            'threshold_high': 150,
        },
        output='M:\\data\\mosamatic\\test\\output',
        overwrite=True,
    )
    task.run()


if __name__ == '__main__':
    test_applythresholdtosegmentations()