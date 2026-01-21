from mosamatic2.core.tasks import TotalSegmentatorTask


def test_totalsegmentator():
    task = TotalSegmentatorTask(
        inputs={'scans': 'M:\\data\\mosamatic\\test\\CT\\abdomen'}, 
        params={
            'tasks': 'total',
            'format': 'dicom',
        },
        output='M:\\data\\mosamatic\\test\\output',
        overwrite=True,
    )
    task.run()