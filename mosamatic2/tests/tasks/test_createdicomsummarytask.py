import os
from mosamatic2.core.tasks.createdicomsummarytask.createdicomsummarytask import CreateDicomSummaryTask


def test_createdicomsummary():
    task = CreateDicomSummaryTask(
        inputs={'directory': 'M:\\data\\mosamatic\\test\\CT\\abdomen'},
        params=None,
        output='M:\\data\\mosamatic\\test\\output',
        overwrite=True,
    )
    task.run()


if __name__ == '__main__':
    test_createdicomsummary()