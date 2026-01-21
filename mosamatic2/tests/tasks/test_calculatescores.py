import os
from mosamatic2.core.tasks.calculatescorestask.calculatescorestask import CalculateScoresTask


def test_calculatescores():
    task = CalculateScoresTask(
        inputs={
            'images': 'M:\\data\\mosamatic\\test\\L3',
            'segmentations': 'M:\\data\\mosamatic\\test\\L3',
            'info': 'M:\\data\\mosamatic\\test\\L3_patient_info\\info.csv',
        },
        params={'file_type': 'npy'},
        output='D:\\Mosamatic\\TestData\\output',
        overwrite=True,
    )
    task.run()
    output_dir = os.path.join(task.output())
    assert os.path.exists(output_dir), 'Output directory does not exist'
    assert len(os.listdir(output_dir)) == 2, 'Output directory does not contain 2 files'
    csv_found, excel_found = False, False
    for f in os.listdir(output_dir):
        if f.endswith('.csv'):
            csv_found = True
        if f.endswith('.xlsx'):
            excel_found = True
    assert csv_found and excel_found, 'CSV or Excel file missing from output'


if __name__ == '__main__':
    test_calculatescores()