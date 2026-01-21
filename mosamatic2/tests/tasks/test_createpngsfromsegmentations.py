from mosamatic2.core.tasks.createpngsfromsegmentationstask.createpngsfromsegmentationstask import CreatePngsFromSegmentationsTask


def test_createpngsfromsegmentationstask():
    task = CreatePngsFromSegmentationsTask(
        inputs={
            'images': 'M:\\data\\mosamatic\\test\\L3',
            'segmentations': 'M:\\data\\mosamatic\\test\\L3'
        }, 
        params={
            'fig_width': 10, 
            'fig_height': 10,
            'hu_low': 30,
            'hu_high': 150,
            'alpha': 1.0,
        },
        output='M:\\data\\mosamatic\\test\\output',
        overwrite=True,
    )
    task.run()