# import os

# from mosamatic.pipelines import DefaultPipeline
# from mosamatic.utils import is_dicom

# from tests.sources import get_sources
# SOURCES = get_sources()


# def test_default_pipeline_tensorflow():
#     assert os.path.exists(SOURCES['input']), 'Input directory does not exist'
#     pipeline = DefaultPipeline(
#         images_dir=SOURCES['input'],
#         model_files_dir=SOURCES['model_files']['tensorflow'],
#         output_dir=SOURCES['output'],
#         target_size=512,
#         model_type='tensorflow',
#         model_version='1.0',
#         fig_width=10,
#         fig_height=10,
#         full_scan=False,
#         overwrite=True,
#     )
#     pipeline.run()
#     check_output(pipeline)


# def test_default_pipeline_pytorch():
#     assert os.path.exists(SOURCES['input']), 'Input directory does not exist'
#     pipeline = DefaultPipeline(
#         images_dir=SOURCES['input'],
#         model_files_dir=SOURCES['model_files']['pytorch'],
#         output_dir=SOURCES['output'],
#         target_size=512,
#         model_type='pytorch',
#         model_version='2.2',
#         fig_width=10,
#         fig_height=10,
#         full_scan=False,
#         overwrite=True,
#     )
#     pipeline.run()
#     check_output(pipeline)


# def check_output(pipeline):

#     output_dir = os.path.join(pipeline.output(), 'DecompressDicomFilesTask')
#     assert os.path.exists(output_dir), 'Output directory does not exist'
#     assert len(os.listdir(output_dir)) == 4, 'Output directory does not contain 4 files'
#     for f in os.listdir(output_dir):
#         assert is_dicom(os.path.join(output_dir, f)), f'File {f} is not DICOM'

#     output_dir = os.path.join(pipeline.output(), 'RescaleDicomFilesTask')
#     assert os.path.exists(output_dir), 'Output directory does not exist'
#     assert len(os.listdir(output_dir)) == 4, 'Output directory does not contain 4 files'
#     for f in os.listdir(output_dir):
#         assert is_dicom(os.path.join(output_dir, f)), f'File {f} is not DICOM'

#     task_name = 'SegmentMuscleFatL3Task' if pipeline.param('model_type') == 'pytorch' else 'SegmentMuscleFatL3TensorFlowTask'
#     output_dir = os.path.join(pipeline.output(), task_name)
#     assert os.path.exists(output_dir), 'Output directory does not exist'
#     assert len(os.listdir(output_dir)) == 4, 'Output directory does not contain 4 files'
#     for f in os.listdir(output_dir):
#         assert f.endswith('.seg.npy'), f'File {f} is not a NumPy file'

#     output_dir = os.path.join(pipeline.output(), 'CalculateScoresTask')
#     assert os.path.exists(output_dir), 'Output directory does not exist'
#     assert len(os.listdir(output_dir)) == 2, 'Output directory does not contain 2 files'
#     assert os.path.exists(os.path.join(output_dir, 'bc_scores.csv'))
#     assert os.path.exists(os.path.join(output_dir, 'bc_scores.xlsx'))

#     output_dir = os.path.join(pipeline.output(), 'CreatePngsFromSegmentationsTask')
#     assert os.path.exists(output_dir), 'Output directory does not exist'
#     assert len(os.listdir(output_dir)) == 4, 'Output directory does not contain 4 files'
#     for f in os.listdir(output_dir):
#         assert f.endswith('.seg.npy.png'), f'File {f} is not a PNG file'