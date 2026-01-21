from mosamatic2.core.pipelines import LiverAnalysisPipeline


def test_liveranalysispipeline():
    pipeline = LiverAnalysisPipeline(
        inputs={'scans': 'M:\\data\\mosamatic\\test\\CT\\abdomen'},
        params={'compressed': True},
        output='M:\\data\\mosamatic\\test\\output',
        overwrite=True,
    )
    pipeline.run()