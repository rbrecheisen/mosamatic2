from mosamatic2.app import run_tests


def test_app():
    assert run_tests() == 'PASSED'