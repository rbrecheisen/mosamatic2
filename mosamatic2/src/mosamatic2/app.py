import sys
import traceback
import faulthandler
import mosamatic2.constants as constants
from PySide6 import QtWidgets
from PySide6 import QtCore
from mosamatic2.ui.settings import Settings
from mosamatic2.core.managers.logmanager import LogManager
from mosamatic2.ui.widgets.splashscreen import SplashScreen
faulthandler.enable(all_threads=True)
LOG = LogManager()


def excepthook(exc_type, exc, tb):
    LOG.error(traceback.format_exc())
    # traceback.print_exception(exc_type, exc, tb)
sys.excepthook = excepthook


def qt_message_handler(msg_type, ctx, msg):
    LOG.error(f"QT[{msg_type}]: {msg} ({ctx.file}:{ctx.line})")
QtCore.qInstallMessageHandler(qt_message_handler)


def run_tests():
    return 'PASSED'


def main():
    settings = Settings()
    application_name = settings.get(constants.MOSAMATIC2_WINDOW_TITLE)
    QtWidgets.QApplication.setApplicationName(application_name)
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName(application_name)
    try:
        splash = SplashScreen()
        splash.show()
        raise SystemExit(app.exec())
        # sys.exit(app.exec())
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        sys.exit(1)

if __name__ == '__main__':
    main()