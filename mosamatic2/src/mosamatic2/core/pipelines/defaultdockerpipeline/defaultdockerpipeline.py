import os

from mosamatic2.core.pipelines.pipeline import Pipeline
from mosamatic2.core.managers.logmanager import LogManager

LOG = LogManager()
DOCKER_SCRIPT = """
docker run --rm ^
    -v "%IMAGES%":/data/images ^
    -v "%MODEL_FILES%":/data/model_files ^
    -v "%OUTPUT%":/data/output ^
    brecheisen/mosamatic2-cli:%VERSION% defaultpipeline ^
        --images /data/images --model_files /data/model_files --output /data/output --overwrite true
"""


class DefaultDockerPipeline(Pipeline):
    INPUTS = [
        'images',
        'model_files',
    ]
    PARAMS = [
        'target_size',
        'file_type',
        'fig_width',
        'fig_height',
        'model_type',
        'model_version',
        'version',
    ]
    def __init__(self, inputs, params, output, overwrite):
        super(DefaultDockerPipeline, self).__init__(inputs, params, output, overwrite)

    def run(self):
        docker_script = 'docker run --rm ' + \
            '-v "{}":/data/images '.format(self.input('images')) + \
            '-v "{}":/data/model_files '.format(self.input('model_files')) + \
            '-v "{}":/data/output '.format(self.output()) + \
            'brecheisen/mosamatic2-cli:{} defaultpipeline '.format(self.param('version')) + \
            '--images /data/images --model_files /data/model_files --output /data/output --overwrite true'
        LOG.info(f'Running Docker script: {docker_script}')
        os.system(docker_script)