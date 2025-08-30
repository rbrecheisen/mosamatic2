import argparse
import mosamatic2.constants as constants
from flask import Flask

app = Flask(__name__)


@app.route('/test')
def run_tests():
    return 'PASSED'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=constants.MOSAMATIC2_SERVER_PORT)
    parser.add_argument('--debug', type=bool, default=constants.MOSAMATIC2_SERVER_DEBUG)
    args = parser.parse_args()
    app.run(host='0.0.0.0', port=args.port, debug=args.debug)