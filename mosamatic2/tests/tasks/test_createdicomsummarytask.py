import os
from mosamatic2.core.tasks.createdicomsummarytask.createdicomsummarytask import CreateDicomSummaryTask


def test_createdicomsummary():
    task = CreateDicomSummaryTask(
        inputs={'directory': 'D:\\Mosamatic\\TestMultiScanUploadMosamatic'},
        params=None,
        output='D:\\Mosamatic\\TestMultiScanUploadMosamatic\\output',
        overwrite=True,
    )
    task.run()


if __name__ == '__main__':
    test_createdicomsummary()