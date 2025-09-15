from PySide6.QtWidgets import (
    QLineEdit,
    QHBoxLayout,
    QVBoxLayout,
    QFormLayout,
    QPushButton,
    QFileDialog,
)
from mosamatic2.ui.widgets.panels.visualizations.visualization import Visualization
from mosamatic2.ui.widgets.panels.visualizations.niftislicevisualization.niftisliceviewer import NiftiSliceViewer
from mosamatic2.core.managers.logmanager import LogManager
from mosamatic2.ui.settings import Settings
from mosamatic2.ui.utils import is_macos

LOG = LogManager()
PANEL_TITLE = 'NiftiSliceVisualization'
PANEL_NAME = 'niftislicevisualization'


class NiftiSliceVisualization(Visualization):
    def __init__(self):
        super(NiftiSliceVisualization, self).__init__()
        self.set_title(PANEL_TITLE)
        self._image_line_edit = None
        self._image_select_button = None
        self._slice_viewer = None
        self._form_layout = None
        self._settings = None
        self.init_layout()

    def image_line_edit(self):
        if not self._image_line_edit:
            self._image_line_edit = QLineEdit(self.settings().get(f'{PANEL_NAME}/image'))
        return self._image_line_edit
    
    def image_select_button(self):
        if not self._image_select_button:
            self._image_select_button = QPushButton('Select')
            self._image_select_button.clicked.connect(self.handle_image_select_button)
        return self._image_select_button
    
    def slice_viewer(self):
        if not self._slice_viewer:
            self._slice_viewer = NiftiSliceViewer()
        return self._slice_viewer

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
        image_layout.addWidget(self.image_line_edit())
        image_layout.addWidget(self.image_select_button())
        self.form_layout().addRow('NIFTI file', image_layout)
        layout = QVBoxLayout()
        layout.addLayout(self.form_layout())
        self.setLayout(layout)
        self.setObjectName(PANEL_NAME)

    def handle_image_select_button(self):
        last_directory = self.settings().get('last_directory')
        directory = QFileDialog.getExistingDirectory(dir=last_directory)
        if directory:
            self.image_line_edit().setText(directory)
            # Load the NIFTI image
            self.settings().set('last_directory', directory)

    def save_inputs_and_parameters(self):
        self.settings().set(f'{PANEL_NAME}/image', self.image_line_edit().text())