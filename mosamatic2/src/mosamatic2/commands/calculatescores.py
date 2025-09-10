import click

from mosamatic2.core.tasks import CalculateScoresTask


@click.command(help='Calculates body composition scores')
@click.option(
    '--images', 
    required=True, 
    type=click.Path(exists=True), 
    help='Directory with images',
)
@click.option(
    '--segmentations',
    required=True,
    type=click.Path(exists=True), 
    help='Directory with segmentations',
)
@click.option(
    '--output', 
    required=True, 
    type=click.Path(), 
    help='Output directory'
)
@click.option(
    '--file_type',
    default='npy',
    help='Options: [npy, tag]'
)
@click.option(
    '--overwrite', 
    type=click.BOOL, 
    default=False, 
    help='Overwrite (true/false)'
)
def calculatescores(images, segmentations, output, file_type, overwrite):
    task = CalculateScoresTask(
        inputs={'images': images, 'segmentations': segmentations},
        params={'file_type': file_type},
        output=output,
        overwrite=overwrite,
    )
    task.run()