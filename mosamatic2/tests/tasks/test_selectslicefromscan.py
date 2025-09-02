# import os

# from mosamatic.tasks import SelectSliceFromScanTask
# from tests.sources import get_sources
# SOURCES = get_sources()


# def test_slice_selection():
#     task = SelectSliceFromScanTask(
#         scans_dir=SOURCES['scans'],
#         output_dir=SOURCES['output'], 
#         vertebral_level='vertebrae_L3',
#         overwrite=True,
#     )
#     task.run()
#     output_dir = os.path.join(SOURCES['output'], 'SelectSliceFromScanTask')
#     assert os.path.exists(output_dir), 'Output directory does not exist'
