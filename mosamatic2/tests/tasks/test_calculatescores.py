import os

from mosamatic2.core.tasks.calculatescorestask.calculatescorestask import CalculateScoresTask
from tests.sources import get_sources
SOURCES = get_sources()


def test_tag():
    task = CalculateScoresTask(
        inputs={
            'images': SOURCES['input'],
            'segmentations': SOURCES['input'],
        },
        params={'file_type': 'tag'},
        output=SOURCES['output'],
        overwrite=True,
    )
    task.run()
    output_dir = os.path.join(SOURCES['output'], 'CalculateScoresTask')
    assert os.path.exists(output_dir), 'Output directory does not exist'
    assert len(os.listdir(output_dir)) == 2, 'Output directory does not contain 2 files'
    csv_found, excel_found = False, False
    for f in os.listdir(output_dir):
        if f.endswith('.csv'):
            csv_found = True
        if f.endswith('.xlsx'):
            excel_found = True
    assert csv_found and excel_found, 'CSV or Excel file missing from output'