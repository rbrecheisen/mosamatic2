import click

from mosamatic2.core.tasks import SegmentMuscleFatL3TensorFlowTask


@click.command(help='Extracts muscle and fat regions from CT images at L3 (uses PyTorch)')
@click.option(
    '--images', 
    required=True, 
    type=click.Path(), 
    help='Input directory with images'
)
@click.option(
    '--model_files', 
    required=True, 
    type=click.Path(), 
    help='Input directory with AI model files'
)
@click.option(
    '--output', 
    required=True, 
    type=click.Path(), 
    help='Output directory'
)
@click.option(
    '--overwrite', 
    default=False, 
    type=click.BOOL, 
    help='Overwrite (true/false)'
)
def segmentmusclefatl3tensorflow(images, model_files, output, overwrite):
    task = SegmentMuscleFatL3TensorFlowTask(
        inputs={'images': images, 'model_files': model_files},
        params={'model_version': 1.0},
        output=output,
        overwrite=overwrite,
    )
    task.run()