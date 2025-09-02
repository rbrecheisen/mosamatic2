from PySide6.QtWidgets import (
    QWidget,
    QDockWidget,
    QTextEdit,
    QPushButton,
    QVBoxLayout,
    QLabel,
)

from mosamatic2.core.managers.logmanagerlistener import LogManagerListener

PANEL_TITLE = 'Output log'
PANEL_NAME = 'logpanel'


class LogPanel(QDockWidget, LogManagerListener):
    def __init__(self):
        super(LogPanel, self).__init__()
        self._title_label = None
        self._text_edit = None
        self.init_layout()

    def title_label(self):
        if not self._title_label:
            self._title_label = QLabel(PANEL_TITLE)
        return self._title_label

    def text_edit(self):
        if not self._text_edit:
            self._text_edit = QTextEdit()
        return self._text_edit
    
    def init_layout(self):
        clear_logs_button = QPushButton('Clear log')
        clear_logs_button.clicked.connect(self.handle_clear_logs_button)
        layout = QVBoxLayout()
        # layout.addWidget(self.title_label())
        layout.addWidget(self.text_edit())
        layout.addWidget(clear_logs_button)
        container = QWidget()
        container.setLayout(layout)
        self.setObjectName(PANEL_NAME)
        self.setWindowTitle(self.title_label().text())
        self.setWidget(container)

    # HELPERS

    def add_line(self, line):
        self.text_edit().insertPlainText(line + '\n')
        self.move_to_end()

    def move_to_end(self):
        cursor = self.text_edit().textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.text_edit().setTextCursor(cursor)
        self.text_edit().ensureCursorVisible()

    # EVENTS

    def handle_clear_logs_button(self):
        self.text_edit().clear()

    # implements(LogManagerListener)
    def new_message(self, message):
        self.add_line(message)