from PySide6.QtWidgets import (
    QLineEdit,
    QHBoxLayout,
    QVBoxLayout,
    QFormLayout,
    QPushButton,
    QFileDialog,
)
from mosamatic2.ui.widgets.panels.visualizations.visualization import Visualization
from mosamatic2.core.managers.logmanager import LogManager
from mosamatic2.ui.settings import Settings
from mosamatic2.ui.utils import is_macos

LOG = LogManager()
PANEL_TITLE = 'LiverSegmentVisualization'
PANEL_NAME = 'liversegmentvisualization'


class LiverSegmentVisualization(Visualization):
    def __init__(self):
        super(LiverSegmentVisualization, self).__init__()
        self.set_title(PANEL_TITLE)
        self._images_line_edit = None
        self._images_dir_select_button = None
        self._load_images_button = None
        self._form_layout = None
        self._settings = None
        self.init_layout()

    def images_line_edit(self):
        if not self._images_line_edit:
            self._images_line_edit = QLineEdit(self.settings().get(f'{PANEL_NAME}/images'))
        return self._images_line_edit
    
    def images_dir_select_button(self):
        if not self._images_dir_select_button:
            self._images_dir_select_button = QPushButton('Select directory')
            self._images_dir_select_button.clicked.connect(self.handle_images_dir_select_button)
        return self._images_dir_select_button
    
    def load_images_button(self):
        if not self._load_images_button:
            self._load_images_button = QPushButton('Load')
            self._load_images_button.clicked.connect(self.handle_load_images_button)
        return self._load_images_button
    
    def form_layout(self):
        if not self._form_layout:
            self._form_layout = QFormLayout()
            if is_macos():
                self._form_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        return self._form_layout

    def settings(self):
        if not self._settings:
            self._settings = Settings()
        return self._settings

    def init_layout(self):
        image_layout = QHBoxLayout()
        image_layout.addWidget(self.images_line_edit())
        image_layout.addWidget(self.images_dir_select_button())
        self.form_layout().addRow('Liver segments directory', image_layout)
        layout = QVBoxLayout()
        layout.addLayout(self.form_layout())
        layout.addWidget(self.load_images_button())
        self.setLayout(layout)
        self.setObjectName(PANEL_NAME)

    def handle_images_dir_select_button(self):
        last_directory = self.settings().get('last_directory')
        dir_path = QFileDialog.getExistingDirectory(dir=last_directory)
        if dir_path:
            self.images_line_edit().setText(dir_path)
            self.settings().set('last_directory', dir_path)

    def handle_output_dir_select_button(self):
        last_directory = self.settings().get('last_directory')
        dir_path = QFileDialog.getExistingDirectory(dir=last_directory)
        if dir_path:
            self.output_dir_line_edit().setText(dir_path)
            self.settings().set('last_directory', dir_path)

    def handle_load_images_button(self):
        pass

    def save_inputs_and_parameters(self):
        self.settings().set(f'{PANEL_NAME}/images', self.images_line_edit().text())