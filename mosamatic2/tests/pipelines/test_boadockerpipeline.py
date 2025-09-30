import os
from mosamatic2.core.pipelines import BoaDockerPipeline
from tests.sources import get_sources

SOURCES = get_sources()


def test_boadockerpipeline():
    assert os.path.exists(SOURCES['scans']), 'Scans directory does not exist'
    pipeline = BoaDockerPipeline(
        inputs={'scans': 'D:\\BOA\\testdata'},
        params=None,
        output='D:\\BOA',
        overwrite=True,
    )
    pipeline.run()
    check_output(pipeline)


def check_output(pipeline):
    pass